$(document).ready (function() {
    $("#compile").click(function() {
        console.log("clicked compile");
        var new_pdf_src = $("#latex_pdf").attr("src");
        var text = $("#latex_editor").val();
        //console.log(text);
        var msg = {'formid': formid,
                   'text': text}
        $.ajax({
            type: "POST", 
            url: "/compile/",
            data: msg,
            success: function(response) {
                console.log(response['error']);
                new_pdf_src = response['output_file'];
                $("#log p").html(response['output_log']).wrap('<pre />');
                $("#latex_pdf").attr("src", new_pdf_src);
                var detached = $("#latex_pdf").detach();
                $(".right_pane").append(detached);
            },
            error: function(xhr, stat, error) {
                console.log(xhr.response);
                console.log(stat);
                console.log(error);
            }
        });
    });

    $("#latex_editor").val(contents);

    $("#save").click(function() {
        var text = $("#latex_editor").val();
        var data_json = {'text': text};
        $.ajax({
            type: "POST", 
            url: "/save/",
            data: text,
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, stat, error) {
                console.log(xhr.response);
                console.log(stat);
                console.log(error);
            }
        });
    });
});

$(document).ready(function() {
    $("#menu ul li a").click(function(e) {
        e.preventDefault();
        
        $("#menu ul li a").each(function() {
            $(this).removeClass("active");  
        });
        
        $(this).addClass("active");
        if ($(this).attr('title') == 'pdf') {
            $("#log").removeClass();
            $("#latex_pdf").removeClass();
            $("#log").addClass("invisible"); 
            $("#latex_pdf").addClass("visible"); 
        }
        if ($(this).attr('title') == 'log') {
            $("#log").removeClass();
            $("#latex_pdf").removeClass();
            $("#log").addClass("visible"); 
            $("#latex_pdf").addClass("invisible"); 
        }
    });
});

//AJAX CSRF stuff 
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
