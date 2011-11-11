# Create your views here.
from django.shortcuts import render_to_response
from multi_editor.models import Doc, DocVersion
from django.conf import settings
import os
import string 
import random
import datetime
from django.http import HttpResponse
from django.utils import simplejson
import shlex
import subprocess

def generate_formid():
    N = 16
    return ''.join(random.choice(string.letters + string.digits) for x in xrange(N))

def get_local_file_path(docVersion):
    return os.path.join(settings.MEDIA_ROOT, docVersion.file_path)

def generate_doc_path(docVersion):
    namespace = docVersion.document.namespace
    print namespace 
    name = docVersion.document.name
    path = os.path.join(
        namespace,
        name,
        str(docVersion.id))
    return path

def get_new_doc_version(doc):
    docVersion = DocVersion(document = doc, 
        contents = '', 
        last_saved = datetime.datetime.now(),
        file_path = '')
    docVersion.save()
    doc.last_version = docVersion
    doc.save()
    docVersion.file_path = generate_doc_path(docVersion)
    docVersion.save()

def display(request, namespace, name):
    try:
        doc = Doc.objects.get(namespace = namespace, name = name)
        docVersion = doc.last_version
        if not docVersion:
            get_new_doc_version(doc)
    except Doc.DoesNotExist:
        mw_formid = generate_formid()
        doc = Doc(namespace = namespace, name = name, mobwrite_formid = mw_formid) 
        doc.save()
        get_new_doc_version(doc)
        docVersion = doc.last_version

    return render_to_response('index.html', 
        {'doc': doc,
         'docVersion': docVersion})

#ajaxified
def save(request):
    if request.is_ajax():
        if request.method == 'POST':
            message = request.POST 
    else:
        message = "Nothing to save"
    return HttpResponse(message)

def create_directory(file_path):
    try:
        os.makedirs(file_path)
    except os.error:
        return False 
    return True

#returns (success, message)
#note that success=True does not mean it compiled correctly
def compile_latex(docVersion, text):
    local_file_path =  get_local_file_path(docVersion)
    create_directory(local_file_path)
    if not os.path.exists(local_file_path):
        return (False, 'could not create file path') 
    source_file = os.path.join(local_file_path, 'source.tex')

    if not text:
        return(False, 'no text to compile')
    
    #format the text
    text = text.replace('\r', '\n')

    with open(source_file, 'w') as f:
        f.write(text)

    #compile that ish
    cmd = '/usr/bin/pdflatex -interaction nonstopmode -halt-on-error -file-line-error -jobname output -output-directory %s %s' %\
          (local_file_path, 'source.tex')
    print cmd
    args = [a.replace('\0', '') for a in shlex.split(cmd)]
    print args
    output, error = subprocess.Popen(args,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE).communicate(str.encode('utf-8'))
    if output:
        output = output.decode('utf-8')
    return (True, output)

def get_pdf_url_from_file(doc_file_path):
    url = os.path.join('/site_media', 'compiled', doc_file_path, 'output.pdf')
    print url
    return url

def compile(request):
    if request.is_ajax():
        message = {'error': 'no error'}
        if request.method == 'POST':
            inp = request.POST
            mw_formid = inp.get('formid', '')
            text = inp.get('text', '')
            if not mw_formid:
                message['error'] = 'could not find the formid'
            try:
                doc = Doc.objects.get(mobwrite_formid = mw_formid)
                docVersion = doc.last_version
                if not docVersion:
                    message['error'] = 'no document version found'
                else:
                    success, output_log = compile_latex(docVersion, text)
                    if not success:
                        message['error'] = output_log
                    message['output_log'] = output_log
                    url = get_pdf_url_from_file(docVersion.file_path)
                    message['output_file'] = url
            except Doc.DoesNotExist:
                message['error'] = 'no docoument found' 
    else:
        message['error'] = 'Nothing to compile'
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')
