from django.db import models

# Create your models here.
class Doc(models.Model):
    namespace = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    last_version = models.ForeignKey('DocVersion', blank=True, null=True)
    mobwrite_formid = models.CharField(max_length = 16)

    class Meta:
        unique_together = ('namespace', 'name')

class DocVersion(models.Model):
    document = models.ForeignKey(Doc)
    contents = models.TextField()
    created = models.DateTimeField(auto_now=True)
    last_saved = models.DateTimeField()
    file_path = models.FilePathField(
        blank = True,
        null = True, 
        path = '/home/sohan/Programming/ourtex/compiled'
    )
