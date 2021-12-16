

var most_read_replies_array = []
var trending_replies_array = []
var trending_replies = []
var inline_loader = "{% include 'custom/inline_loading.html' %}"
var recommended_inline_loader = "{% include 'custom/recommended_inline_loading.html' %}"
var inline_loader_small = "{% include 'custom/inline_loading_small.html' %}"
var inline_loader_small_center = "{% include 'custom/inline_loading_small_center.html' %}"
var inline_loader_small_center_absolute = "{% include 'custom/inline_loading_small_center_absolute.html' %}"

var most_read_replies = []
var interest_replies = []
var interest_replies_array = []

var recommended_replies = []
var recommended_replies_array = []
var related_replies = []
var related_replies_array = []
var recent_replies = []
var recent_replies_array = []
var random_recommended = []
var random_recommended_array = []


var popular_libraries = []
var popular_libraries_array = []




{
    (function ($) { //Most read async
        $('.load-main-content-btn').on('click', function () {
           
            var link = $(this);
            $.ajax({
                beforeSend: function () {
                    
                        $('#main-content').append(inline_loader_small_center);
                        
                    
                },
                complete: function () {
                    $('#main-content').children('.loading').remove()
                },
                type: 'get',
                url: link.attr('contenturl'),
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (response) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    // append html to the posts div
                    //$('.uk-modal-header-title').empty()

                    //$('.uk-modal-header-title').append(link.attr('inner-html'));
                    $('#page-header').empty()
                    $('#page-header').append(response.header);
                    $('#main-content').empty();
                    $('#main-content').append(response.content);
                     

                    },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};



{
    (function ($) { //Most read async
        $('.signout').on('click', function () {
           
            logout()
        });
    }(jQuery))
};



{
    (function ($) { //Most read async
        $('.modal-btn').on('click', function () {
            alert('clicked')
            $('.uk-modal-body').empty()
            var link = $(this);
            $.ajax({
                beforeSend: function () {
                    
                        $('.uk-modal-body').append(inline_loader_small_center);
                        
                    
                },
                complete: function () {
                    $('.uk-modal-body').children('.loading').remove()
                },
                type: 'get',
                url: link.attr('contenturl'),
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    // append html to the posts div
                    //$('.uk-modal-header-title').empty()

                    //$('.uk-modal-header-title').append(link.attr('inner-html'));
                    $('.uk-modal-body').append(data.message);
                   
                     

                    },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};




$("#commentform").submit(function(event){
    event.preventDefault(); //prevent default action 
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
	var form_data = new FormData(this); //Creates new FormData object
    $.ajax({
        beforeSend: function () {
            UIkit.notification('Posting'+inline_loader_small)
               
            
        },
        complete: function () {
           
           
        },
        url : post_url,
        type: request_method,
        data : form_data,
		contentType: false,
		cache: false,
        processData:false,    
    
        success: function (data) {
            // if there are still more pages to load,
            // add 1 to the "Load More Posts" link's page data attribute
            // else hide the link
            
            // append html to the posts div
            $('#commentscontainer').append(data.comment_html);
            $('.csrf').val(window.CSRF_TOKEN)
            if (data.commented){
                UIkit.notification.closeAll()
            UIkit.notification('Commented')

            }
            else{
                alert(response.posted)
                UIkit.notification.closeAll()
            UIkit.notification('Unauthorized operation',)
        }
    },
        error: function (xhr, status, error) {
            UIkit.notification.closeAll()
            UIkit.notification('Not sent. Check your internet connection',)
        }});
});


$("#asyncform").submit(function(event){
    event.preventDefault(); //prevent default action 
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
	var form_data = new FormData(this); //Creates new FormData object
    $.ajax({
        beforeSend: function () {
            UIkit.notification('Posting'+inline_loader_small)
               
            
        },
        complete: function () {
           
           
        },
        url : post_url,
        type: request_method,
        data : form_data,
		contentType: false,
		cache: false,
        processData:false,    
    
        success: function (data) {
            // if there are still more pages to load,
            // add 1 to the "Load More Posts" link's page data attribute
            // else hide the link
            
            // append html to the posts div
            if (data.posted){
                UIkit.notification.closeAll()
            UIkit.notification(data.message)

            }
            else{
                alert(response.posted)
                UIkit.notification.closeAll()
            UIkit.notification('Unauthorized operation',)
        }
    },
        error: function (xhr, status, error) {
            UIkit.notification.closeAll()
            UIkit.notification('Not sent. Check your internet connection',)
        }});
});



{
    (function ($) { //Most read async
        $('.delete-btn').on('click', function () {
            var deleteButton = $(this);
            var deleteUrl = deleteButton.attr('durl')
            $.ajax({
                beforeSend: function () {
                    UIkit.notification.closeAll()
                    UIkit.notification('Deleting'+inline_loader_small)
                       
                    
                },
                complete: function () {
                   

                },
                type: 'post',
                url: deleteUrl,
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    
                    // append html to the posts div
                    if (data.deleted){
                        UIkit.notification.closeAll()
                    UIkit.notification(data.message)
                    $('#'+deleteButton.attr('content')).remove()

                    }
                    else if(data.authorized == False) {
                        alert(response.posted)
                        UIkit.notification.closeAll()
                    UIkit.notification('Unauthorized operation',)

                }
            },
                error: function (xhr, status, error) {
                    UIkit.notification.closeAll()
                    UIkit.notification('Delete not successful. Check your internet connection',)
                }
            });
        });
    }(jQuery))
};



{% for comment in comments %}
{
    (function ($) { //Most read async
        $('#{{comment.comment_id}}repliesmore').on('click', function () {
            var link = $(this);
            var newreplies = link.data('page');
            
            $.ajax({
                beforeSend: function () {
                    
                        $('#{{comment.comment_id}}repliescontainer').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#{{comment.comment_id}}repliescontainer').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "replies" comment_id=comment.comment_id episode_id=episode.episode_id %}',
                data: {
                    'newreplies': newreplies,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    
                    // append html to the posts div

                    $('#{{comment.comment_id}}repliescontainer').append(data.replies_html);
                    if (data.has_next) {
                        $('.{{comment.comment_id}}replies2').css('display','block')

                        $('.{{comment.comment_id}}replies').data('page', newreplies + 1);
                    } else {
                    $('.{{comment.comment_id}}replies2').css('display','none')
                      $('.{{comment.comment_id}}replies1').attr('class','disabled uk-disabled')

                    }

                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{% endfor %}