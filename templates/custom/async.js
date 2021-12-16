var savedStoryLoaded = false
var trendingStoryLoaded = false
var mostReadStoryLoaded = false
var interestStoriesLoaded = false
var recommendedStoriesLoaded = false
var popularLibrariesLoaded = false
var LibraryStoryLoaded = false
var darkMode = {% if currentuser.dark_mode %} true {% else %} false {% endif %}

var most_read_stories_array = []
var trending_stories_array = []
var trending_stories = []
var inline_loader = "{% include 'custom/inline_loading.html' %}"
var recommended_inline_loader = "{% include 'custom/recommended_inline_loading.html' %}"
var inline_loader_small_center = "{% include 'custom/inline_loading_small_center.html' %}"

var most_read_stories = []
var interest_stories = []
var interest_stories_array = []

var recommended_stories = []
var recommended_stories_array = []
var related_stories = []
var related_stories_array = []
var recent_stories = []
var recent_stories_array = []
var random_recommended = []
var random_recommended_array = []


var popular_libraries = []
var popular_libraries_array = []
var scene = 2


{
    (function ($) { //Most read async
        $('.switch-paddle.theme').on('click', function () {
            if(darkMode == true){
                var sheet = (function() {
                    // Create the <style> tag
                    var style = document.createElement("style");
                
                    // Add a media (and/or media query) here if you'd like!
                    // style.setAttribute("media", "screen")
                    // style.setAttribute("media", "only screen and (max-width : 1024px)")
                
                    // WebKit hack :(
                    style.appendChild(document.createTextNode(""));
                
                    // Add the <style> element to the page
                    document.head.appendChild(style);
                
                    return style.sheet;
                })();

                sheet.insertRule(".dark-mode { background-color: white ; color: black ; }");
                sheet.insertRule(".dark-mode-light-force { background-color: white ; color: black ; }");
                sheet.insertRule(".dark-mode-no-background {color: black ; }");
                sheet.insertRule(".text-sm {color: black ; }");
                sheet.insertRule('#storypalm{-webkit-filter: brightness(1) invert(0);filter: invert(0) brightness(1) ;}')
                sheet.insertRule(".form-control {color: black ; }");

                darkMode = false
                $.ajax({
                    beforeSend: function () {
                        
                        
                    },
                    complete: function () {
                    },
                    type: 'post',
                    url: '{% url "theme" %}',
                    data: {
                        'theme': 'light',
                        'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    },
                    success: function (data) {
                        
                    },
                    error: function (xhr, status, error) {
                        alert('there was an error')
                    }
                });
                     }

            else{
                var sheet = (function() {
                    // Create the <style> tag
                    var style = document.createElement("style");
                
                    // Add a media (and/or media query) here if you'd like!
                    // style.setAttribute("media", "screen")
                    // style.setAttribute("media", "only screen and (max-width : 1024px)")
                
                    // WebKit hack :(
                    style.appendChild(document.createTextNode(""));
                
                    // Add the <style> element to the page
                    document.head.appendChild(style);
                
                    return style.sheet;
                })();

                sheet.insertRule(".dark-mode { background-color: black ; color: silver ; }");
                sheet.insertRule(".dark-mode-light-force { background-color: rgb(43, 41, 41) ; color: silver ; }");
                sheet.insertRule(".dark-mode-no-background {color: silver ; }");
                sheet.insertRule(".text-sm {color: silver ; }");
                sheet.insertRule('#storypalm{-webkit-filter: brightness(0) invert(1);filter: invert(1) brightness(10) ;}')
                sheet.insertRule(".form-control {color: white ; }");

                darkMode = true
                $.ajax({
                    beforeSend: function () {
                        
                        
                    },
                    complete: function () {
                    },
                    type: 'post',
                    url: '{% url "theme" %}',
                    data: {
                        'theme': 'dark',
                        'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    },
                    success: function (data) {
                        
                    },
                    error: function (xhr, status, error) {
                        alert('there was an error')
                    }
                });
            }
          
        });
    }(jQuery))
};


 // Story async
 if ('{{episode.episode_id}}'){
    {
       (function ($) {
           $('body').ready(function () {
   
               $.ajax({
                   beforeSend: function () {
                       
                       
                   },
                   complete: function () {
                   },
                   type: 'post',
                   url: '{% url "related_episodes" %}',
                   data: {
                       'story_id': '{{episode.story.story_id}}',
                       'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                   },
                   success: function (data) {
                       
   
                       $('#related-episodes').append(data.related_episodes_html);
                       
                   },
                   error: function (xhr, status, error) {
                       alert('there was an error')
                   }
               });
   
           });
       }(jQuery))
   };}
    //Story async

/*  
{% if episode.episode_id %}
{
    (function ($) { //Most read async
      $('.next-scene-btn').ready( function () {
       
                var scene = 1

                $.ajax({
                    
                    type: 'post',
                    url: '{% url "next_scene" episodeid=episode.episode_id %}',
                    data: {
                        'newscene': scene,
                        'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    },
                    success: function (data) {
                        // if there are still more pages to load,
                        // add 1 to the "Load More Posts" link's page data attribute
                        // else hide the link
                       /* if (data.has_next) {
                            
                            $('#loadlibrarystories').data('page', newstories + 1);
                        } else {
                            $('#loadlibrarystories').hide();
                        }
                        // append html to the posts div 
                        if(data.has_next){
                            $('#next-scene-btn').removeClass('uk-hidden uk-invisible')
                        }
                       

                        scene = scene+1
                    },
                    error: function (xhr, status, error) {
                        alert('there was an error')
                    }
                });
            
            }
      )}(jQuery));
};

{% endif %}


{% if episode.episode_id %}

$.fn.nextScene = function(){ 
        
                if (scene != false){
                   
                $.ajax({
                    beforeSend: function () {
                        $('.next-scene').append(inline_loader_small_center);
                    },
                    complete: function () {
                       
                    },
                    type: 'post',
                    url: '{% url "next_scene" episodeid=episode.episode_id %}',
                    data: {
                        'newscene': scene,
                        'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    },
                    success: function (data) {
                        // if there are still more pages to load,
                        // add 1 to the "Load More Posts" link's page data attribute
                        // else hide the link
                       /* if (data.has_next) {
                            
                            $('#loadlibrarystories').data('page', newstories + 1);
                        } else {
                            $('#loadlibrarystories').hide();
                        }
                        // append html to the posts div 
                        $('.next-scene').children('.loading').remove()
                          $('.next-scene').append(data.scene_html);
                        if(data.has_next){
                            $('.next-scene').removeClass('next-scene')
                            $('.scene-container').append('<li class="next-scene col-cmd-14 col-csx-14  col-csxx-14 col-csl-14 col-csm-14 col-css-14 col-csxx-x-14 col-csxx-xx-14 uk-padding-small"></li>')
                        
                            scene = scene+1
                        }

                        else{
                            scene = false
                        }
                        
                    },
                    error: function (xhr, status, error) {
                        alert('there was an error')
                    }
                });
                }
            }

{% endif %}

if('{{episode.story.story_id}}'){
document.getElementById('next-scene-btn').addEventListener('click',$.fn.nextScene )
}
*/

{% if library.library_id %}

{
    (function ($) { //Most read async
      $('.subscribe').on('click', function () {
        var subscribeButton = $(this);
        var subscribeUrl = subscribeButton.attr('contenturl')
        $.ajax({
          beforeSend: function () {
            UIkit.notification.closeAll()


          },
          complete: function () {


          },
          type: 'post',
          url: subscribeUrl,
          data: {
            'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
          },
          success: function (data) {
            // if there are still more pages to load,
            // add 1 to the "Load More Posts" link's page data attribute
            // else hide the link

            // append html to the posts div
            if (data.subscribed) {
                alert(data.subscribed)
                UIkit.notification.closeAll()
                UIkit.notification(data.message)
                subscribeButton.html('unsubscribe')
                subscribeButton.attr('contenturl', '{% url 'library_unsubscribe' libid=library.library_id %}')
  
              }
              else if (data.unsubscribed) {
                UIkit.notification.closeAll()
                UIkit.notification(data.message)
                subscribeButton.html('subscribe')
                subscribeButton.attr('contenturl', '{% url 'library_subscribe' libid=library.library_id %}')
  
              }
          },
          error: function (xhr, status, error) {
            UIkit.notification.closeAll()
            UIkit.notification('subscribe not successful. Check your internet connection',)
          }
        });
      });
    }(jQuery))
  };

{% endif %}


$.fn.writerStoryContent = function(storyContentContainer, contentid,contenturl){ 

    var contentid = contentid
    var storyContentContainer =storyContentContainer;
    $.ajax({
        beforeSend: function () {
            $('#'+storyContentContainer).append(inline_loader_small_center);
        },
        complete: function () {
            $('#'+storyContentContainer).children('.loading').remove()
        },
        
        type: 'post',
        url: contenturl,
        data: {
            'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
        },
        success: function (data) {
            // if there are still more pages to load,
            // add 1 to the "Load More Posts" link's page data attribute
            // else hide the link
           
            $('#'+storyContentContainer).append(data.content_html)
        },
        error: function (xhr, status, error) {
            alert('there was an error')
        }
    });
}




$.fn.loadFormContents= function(contenturl, contenthtml,){ 

   
    $('.uk-modal-body').empty()
    $.ajax({
        beforeSend: function () {
            
                $('.uk-modal-body').append(inline_loader_small_center);
                
            
        },
        complete: function () {
            $('.uk-modal-body').children('.loading').remove()
        },
        type: 'get',
        url: contenturl,
        data: {
            'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
        },
        success: function (data) {
            // if there are still more pages to load,
            // add 1 to the "Load More Posts" link's page data attribute
            // else hide the link
            // append html to the posts div
            $('.uk-modal-header-title').empty()

            $('.uk-modal-header-title').append(contenthtml);
            $('.uk-modal-body').append(data.modal_html);

            $('.csrf').val(window.CSRF_TOKEN)

            },
        error: function (xhr, status, error) {
            alert('there was an error')
        }
    });

}



$.fn.readerStoryContent = function(storyContentContainer, contentid,contenturl){ 

            var contentid = contentid
            var storyContentContainer =storyContentContainer;
            $.ajax({
                beforeSend: function () {
                },
                complete: function () {
                },
                
                type: 'post',
                url: contenturl,
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                   
                    $('.'+storyContentContainer).append(data.content_html)
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
}
    
{
    (function ($) { //Most read async
        $('#loadmostread').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            most_read_stories = document.querySelectorAll('.mostread')
            for (let i = 0; i < most_read_stories.length; i++) {
                most_read_stories_array.push(most_read_stories[i].id)
            }
            $.ajax({
                beforeSend: function () {
                  
                        $('#mostreadstories').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#mostreadstories').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "most_read_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'mostreadidarray': most_read_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#mostreadstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        most_read_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.mostreadidarray.length; i++) {
                        most_read_stories_array.push(data.mostreadidarray[i])
                    }
                    most_read_stories = document.querySelectorAll('.mostread')
                    for (let i = 0; i < most_read_stories.length; i++) {
                        most_read_stories_array.push(most_read_stories[i].id)
                    }

                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};


{
    $.fn.loadMostReadStory = function(){ 
        var newstories = 1;
            var newstories = 1;
            $.ajax({
                beforeSend: function () {
                                        
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "most_read_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'mostreadidarray': most_read_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        $('#loadmostread').data('page', newstories + 1);
                    } else {
                        $('#loadmostread').hide();
                    }
                    // append html to the posts div

                    $('#mostreadstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        most_read_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.mostreadidarray.length; i++) {
                        most_read_stories_array.push(data.mostreadidarray[i])
                    }
                    most_read_stories = document.querySelectorAll('.mostread')
                    for (let i = 0; i < most_read_stories.length; i++) {
                        most_read_stories_array.push(most_read_stories[i].id)
                    }
                    ;
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

    }
};
//Most read async


{
    (function ($) { //Trending async
        $('#loadtrendingstories').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            trending_stories = document.querySelectorAll('.trendingstory')
            for (let i = 0; i < trending_stories.length; i++) {
                trending_stories_array.push(trending_stories[i].id)
            }
            $.ajax({
                beforeSend: function () {
                   
                    
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "trending_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'trendingstoriesidarray': trending_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#trendingstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        trending_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.trendingstoriesidarray.length; i++) {
                        trending_stories_array.push(data.trendingstoriesidarray[i])
                    }
                    trending_stories = document.querySelectorAll('.trendingstory')
                    for (let i = 0; i < trending_stories.length; i++) {
                        trending_stories_array.push(trending_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{
    $.fn.loadTrendingStory = function(){ 
            var newstories = 1;
            $.ajax({
                beforeSend: function () {
                                       
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "trending_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'trendingstoriesidarray': trending_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        $('#loadtrendingstories').data('page', newstories + 1);
                    } else {
                        $('#loadtrendingstories').hide();
                    }
                    // append html to the posts div

                    $('#trendingstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        trending_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.trendingstoriesidarray.length; i++) {
                        trending_stories_array.push(data.trendingstoriesidarray[i])
                    }
                    trending_stories = document.querySelectorAll('.trendingstory')
                    for (let i = 0; i < trending_stories.length; i++) {
                        trending_stories_array.push(trending_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

};
}
//Trending Stories async


{
    (function ($) { //Interests async
        $('#loadintereststories').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            interest_stories = document.querySelectorAll('.intereststory')
            for (let i = 0; i < interest_stories.length; i++) {
                interest_stories_array.push(interest_stories[i].id)
            }
            $.ajax({
                beforeSend: function () {
                    
                        $('#intereststories').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#intereststories').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "interest_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'intereststoriesidarray': interest_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#intereststories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        interest_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.intereststoriesidarray.length; i++) {
                        interest_stories_array.push(data.intereststoriesidarray[i])
                    }
                    interest_stories = document.querySelectorAll('.intereststory')
                    for (let i = 0; i < interest_stories.length; i++) {
                        interest_stories_array.push(interest_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{
    $.fn.loadInterestStory = function(){ 
           
        var newstories = 1;

            $.ajax({
                beforeSend: function () {
                    
                    
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "interest_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'intereststoriesidarray': interest_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        $('#loadintereststories').data('page', newstories + 1);
                    } else {
                        $('#loadintereststories').hide();
                    }
                    // append html to the posts div

                    $('#intereststories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        interest_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.intereststoriesidarray.length; i++) {
                        interest_stories_array.push(data.intereststoriesidarray[i])
                    }
                    interest_stories = document.querySelectorAll('.intereststory')
                    for (let i = 0; i < interest_stories.length; i++) {
                        interest_stories_array.push(interest_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
    }
};
 //Interests Stories async


 
{
    (function ($) { //recommended async
        $('#loadrecommendedstories').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            recommended_stories = document.querySelectorAll('.recommendedstory')
            for (let i = 0; i < recommended_stories.length; i++) {
                recommended_stories_array.push(recommended_stories[i].id)
            }
            $.ajax({
                beforeSend: function () {

                        $('#recommendedstories').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#recommendedstories').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "recommended_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'recommendedstoriesidarray': recommended_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#recommendedstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        recommended_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.recommendedstoriesidarray.length; i++) {
                        recommended_stories_array.push(data.recommendedstoriesidarray[i])
                    }
                    recommended_stories = document.querySelectorAll('.recommendedstory')
                    for (let i = 0; i < recommended_stories.length; i++) {
                        recommended_stories_array.push(recommended_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{
    $.fn.loadRecommendedStory = function(){ 
           
        var newstories = 1;

            $.ajax({
                beforeSend: function () {
                    
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "recommended_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'recommendedstoriesidarray': recommended_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        $('#loadrecommendedstories').data('page', newstories + 1);
                    } else {
                        $('#loadrecommendedstories').hide();
                    }
                    // append html to the posts div

                    $('#recommendedstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        recommended_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.recommendedstoriesidarray.length; i++) {
                        recommended_stories_array.push(data.recommendedstoriesidarray[i])
                    }
                    recommended_stories = document.querySelectorAll('.recommendedstory')
                    for (let i = 0; i < recommended_stories.length; i++) {
                        recommended_stories_array.push(recommended_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
    }
};
 //recommended Stories async

   //Popular libraries async
{
    (function ($) { //popular libraries async
        $('#loadpopularlibraries').on('click', function () {
            var link = $(this);
            var newlibraries = link.data('page');
            popular_libraries = document.querySelectorAll('.popularlibrary')
            for (let i = 0; i < popular_libraries.length; i++) {
                popular_libraries_array.push(popular_libraries[i].id)
            }
            $.ajax({
                beforeSend: function () {
                   
                        $('#popularlibraries').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#popularlibraries').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "popular_libraries" %}',
                data: {
                    'newlibraries': newlibraries,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'popularlibrariesidarray': popular_libraries_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newlibraries + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#popularlibraries').append(data.libraries_html);
                    for (let i = 0; i < data.loadedlibrariesids.length; i++) {
                        popular_libraries_array.push(data.loadedlibrariesids[i])
                    }

                    for (let i = 0; i < data.popularlibrariesidarray.length; i++) {
                        popular_libraries_array.push(data.popularlibrariesidarray[i])
                    }
                    popular_libraries = document.querySelectorAll('.popularlibrary')
                    for (let i = 0; i < popular_libraries.length; i++) {
                        popular_libraries_array.push(popular_libraries[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{

    $.fn.loadPopularLibraries = function(){ 
           
        var newlibraries = 1;
            $.ajax({
                beforeSend: function () {
                   
                    
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "popular_libraries" %}',
                data: {
                    'newlibraries': newlibraries,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'popularlibrariesidarray': popular_libraries_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        $('#loadpopularlibraries').data('page', newlibraries + 1);
                    } else {
                        $('#loadpopularlibraries').hide();
                    }
                    // append html to the posts div

                    $('#popularlibraries').append(data.libraries_html);
                    for (let i = 0; i < data.loadedlibrariesids.length; i++) {
                        popular_libraries_array.push(data.loadedlibrariesids[i])
                    }
                    for (let i = 0; i < data.popularlibrariesidarray.length; i++) {
                        popular_libraries_array.push(data.popularlibrariesidarray[i])
                    }
                    popular_libraries = document.querySelectorAll('.popularlibrary')
                    for (let i = 0; i < popular_libraries.length; i++) {
                        popular_libraries_array.push(popular_libraries[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

            }
}
 //Popular libraries async


  
{
    (function ($) { //recent async
        $('#loadrecentstories').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            recent_stories = document.querySelectorAll('.recentstory')
            for (let i = 0; i < recent_stories.length; i++) {
                recent_stories_array.push(recent_stories[i].id)
            }
            $.ajax({
                beforeSend: function () {
                                       
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "recent_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'recentstoriesidarray': recent_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#recentstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        recent_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.recentstoriesidarray.length; i++) {
                        recent_stories_array.push(data.recentstoriesidarray[i])
                    }
                    recent_stories = document.querySelectorAll('.recentstory')
                    for (let i = 0; i < recent_stories.length; i++) {
                        recent_stories_array.push(recent_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{
    (function ($) {
        $('#recentstories').ready(function () {
            var link = $(this);

            var newstories = link.data('page');
            $.ajax({
                beforeSend: function () {
                   
                    
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "recent_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'recentstoriesidarray': recent_stories_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        $('#loadrecentstories').hide();
                    }
                    // append html to the posts div

                    $('#recentstories').append(data.stories_html);
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        recent_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.recentstoriesidarray.length; i++) {
                        recent_stories_array.push(data.recentstoriesidarray[i])
                    }
                    recent_stories = document.querySelectorAll('.recentstory')
                    for (let i = 0; i < recent_stories.length; i++) {
                        recent_stories_array.push(recent_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        });
    }(jQuery))
};
 //recent Stories async



 // Story async
 if ('{{story.story_id}}'){
 {
    (function ($) {
        $('#story-cont').ready(function () {
            var link = $(this);

            var newstories = link.data('page');
            $.ajax({
                beforeSend: function () {
                    
                    
                },
                complete: function () {
                },
                type: 'post',
                url: '{% url "current_story" %}',
                data: {
                    'story_id': '{{story.story_id}}',
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    

                    $('#story-cont').append(data.story_html);
                    
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        });
    }(jQuery))
};}
 //Story async

   
{
    (function ($) { //random Recommended async
        $('#loadrandomrecommended').on('click', function () {
            var link = $(this);
            
            var newrandomrecommended = link.data('page');
            random_recommended = document.querySelectorAll('.randomrecommended')
            for (let i = 0; i < random_recommended.length; i++) {
                random_recommended_array.push(random_recommended[i].id)
            }
            $.ajax({
                beforeSend: function () {
                   
                      
                    
                },
                complete: function () {
                 

                },
                type: 'post',
                url: '{% url "random_recommended" %}',
                data: {
                    'newrandomrecommended': newrandomrecommended,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'randomrecommendedidarray': random_recommended_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newrandomrecommended + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#randomrecommended').append(data.random_recommended_html);
                    for (let i = 0; i < data.loadedrandomrecommendedids.length; i++) {
                        random_recommended_array.push(data.loadedrandomrecommendedids[i])
                    }

                    for (let i = 0; i < data.randomrecommendedidarray.length; i++) {
                        random_recommended_array.push(data.randomrecommendedidarray[i])
                    }
                    random_recommended = document.querySelectorAll('.randomrecommended')
                    for (let i = 0; i < random_recommended.length; i++) {
                        random_recommended_array.push(random_recommended[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

{
    (function ($) {
        $('#randomrecommended').ready(function () {
            var link = $(this);
            $('#storyabout').remove();

            var newrandomrecommended = link.data('page');
            $.ajax({
                beforeSend: function () {
                   
                     
                    
                },
                complete: function () {
                   
                },
                type: 'post',
                url: '{% url "random_recommended" %}',
                data: {
                    'newrandomrecommended': newrandomrecommended,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'randomrecommendedidarray': random_recommended_array
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newrandomrecommended + 1);
                    } else {
                        $('#loadrandomrecommended').hide();
                    }
                    // append html to the posts div

                    $('#randomrecommended').append(data.random_recommended_html);
                    for (let i = 0; i < data.loadedrandomrecommendedids.length; i++) {
                        random_recommended_array.push(data.loadedrandomrecommendedids[i])
                    }
                    for (let i = 0; i < data.randomrecommendedidarray.length; i++) {
                        random_recommended_array.push(data.randomrecommendedidarray[i])
                    }
                    random_recommended = document.querySelectorAll('.randomrecommended')
                    for (let i = 0; i < random_recommended.length; i++) {
                        random_recommended_array.push(random_recommended[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        });
    }(jQuery))
};
 //recent Stories async

if ('{{story.story_id}}' || '{{episode.story.story_id}}'){
   
{
    (function ($) { //recent async
        $('#loadrelatedstories').on('click', function () {
            var link = $(this);
            var newstories = link.data('page');
            related_stories = document.querySelectorAll('.relatedstory')
            for (let i = 0; i < related_stories.length; i++) {
                related_stories_array.push(related_stories[i].id)
            }
            var story_id = ''
            if('{{episode.story.story_id}}'){
                story_id='{{episode.story.story_id}}'
                
            }
            else{
                story_id='{{story.story_id}}'
            }
            $.ajax({
                beforeSend: function () {
                   
                        $('#relatedstories').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#relatedstories').children('.loading').remove()

                },
                type: 'post',
                url: '{% url "related_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'relatedstoriesidarray': related_stories_array,
                    'story_id': story_id,
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        link.hide();
                    }
                    // append html to the posts div

                    $('#relatedstories').append(data.stories_html);
                    if('{{episode.story.story_id}}'){
                       $('.relatedstory').attr('class','col-cmd-7 col-csl-7 col-csm-14 col-csx-5-e col-csxx-7 col-csxx-xx-7 col-csxx-x-14 col-css-4-e')

                    }
                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        related_stories_array.push(data.loadedstoryids[i])
                    }

                    for (let i = 0; i < data.relatedstoriesidarray.length; i++) {
                        related_stories_array.push(data.relatedstoriesidarray[i])
                    }
                    related_stories = document.querySelectorAll('.relatedstory')
                    for (let i = 0; i < related_stories.length; i++) {
                        related_stories_array.push(related_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};

if ('{{story.story_id}}' || '{{episode.story.story_id}}'){

{
    (function ($) {
        $('#relatedstories').ready(function () {
            var link = $(this);

            var newstories = link.data('page');
            var story_id = ''
            if('{{episode.story.story_id}}'){
                story_id='{{episode.story.story_id}}'
            }
            else{
                story_id='{{story.story_id}}'
            }
            $.ajax({
                beforeSend: function () {
                   
                        $('#relatedstories').append(inline_loader_small_center);
                    
                },
                complete: function () {
                    $('#relatedstories').children('.loading').remove()
                },
                type: 'post',
                url: '{% url "related_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                    'relatedstoriesidarray': related_stories_array,
                    'story_id': story_id
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        link.data('page', newstories + 1);
                    } else {
                        $('#loadrelatedstories').hide();
                    }
                    // append html to the posts div

                    $('#relatedstories').append(data.stories_html);

                    if('{{episode.story.story_id}}'){
                        $('.relatedstory').attr('class','col-cmd-7 col-csl-7 col-csm-14 col-csx-5-e col-csxx-7 col-csxx-xx-7 col-csxx-x-14 col-css-4-e')
 
                     }

                    for (let i = 0; i < data.loadedstoryids.length; i++) {
                        related_stories_array.push(data.loadedstoryids[i])
                    }
                    for (let i = 0; i < data.relatedstoriesidarray.length; i++) {
                        related_stories_array.push(data.relatedstoriesidarray[i])
                    }
                    related_stories = document.querySelectorAll('.relatedstory')
                    for (let i = 0; i < related_stories.length; i++) {
                        related_stories_array.push(related_stories[i].id)
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        });
    }(jQuery))
};
 //related Stories async
}
}

{% if library.library_id %}
{
    (function ($) {
        $('#loadlibrarystories').ready(function (e) {
           
           if(LibraryStoryLoaded){
              
           }
           else{ 
               LibraryStoryLoaded = true
            var newstories = 1
            $.ajax({
                beforeSend: function () {
                },
                complete: function () {
                    LibraryStoryLoaded = false
                },
                type: 'post',
                url: '{% url "my_library_stories" libid=library.library_id %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        
                        $('#loadlibrarystories').data('page', newstories + 1);
                    } else {
                        $('#loadlibrarystories').hide();
                    }
                    // append html to the posts div

                    $('#librarystories').append(data.library_stories_html);

                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        }
        });
    
    return}(jQuery))
};

    


{
    (function ($) {
        $('#loadlibrarystories').on('click',function () {
           
            if(LibraryStoryLoaded){
            }
            else{ 
                LibraryStoryLoaded= true
                 var link = $(this);

            var newstories = link.data('page');
            $.ajax({
                beforeSend: function () {
                                        
                },
                complete: function () {
                    LibraryStoryLoaded= false
                },
                type: 'post',
                url: '{% url "my_library_stories" libid=library.library_id %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        
                        link.data('page', newstories + 1);
                    } else {
                        $('#loadlibrarystories').hide();
                    }
                    // append html to the posts div

                    $('#librarystories').append(data.library_stories_html);
                    
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });}

        });
        
    return}(jQuery))
};

{% endif %}






{
    $.fn.loadSavedStory = function(){ 
        
            var newstories = 1;

            $.ajax({
                beforeSend: function () {
                  
                    
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "my_saved_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        
                        $('#loadsavedstories').data('page', newstories + 1);
                    } else {
                        $('#loadsavedstories').hide();
                    }
                    // append html to the posts div

                    $('#savedstories').append(data.saved_stories_html);

                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

};
}



{
    (function ($) {
        $('#loadsavedstories').on('click',function () {
            var link = $(this);

            var newstories = link.data('page');
            $.ajax({
                beforeSend: function () {
                                        
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "my_saved_stories" %}',
                data: {
                    'newstories': newstories,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if (data.has_next) {
                        
                        link.data('page', newstories + 1);
                    } else {
                        $('#loadsavedstories').hide();
                    }
                    // append html to the posts div

                    $('#savedstories').append(data.saved_stories_html);
                    
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        });
    }(jQuery))
};



if($('#savedstories').visible()){
$.fn.loadSavedStory()
savedStoryLoaded = true
}



    

if($('#trendingstories').visible()){
$.fn.loadTrendingStory()
trendingStoryLoaded= true
}

if($('#mostreadstories').visible()){
$.fn.loadMostReadStory()
mostReadStoryLoaded=true
}

if($('#intereststories').visible()){
$.fn.loadInterestStory()
interestStoriesLoaded = true
}


if($('#recommendedstories').visible()){
$.fn.loadRecommendedStory()
recommendedStoriesLoaded = true
}



if($('#popularlibraries').visible()){
$.fn.loadPopularLibraries()
popularLibrariesLoaded = true
}




$( window ).scroll(function() {

    
 
        
    if(savedStoryLoaded){}
    else{
  if($('#savedstories').visible()){
    $.fn.loadSavedStory()
savedStoryLoaded = true
  }

    }
  

    if(trendingStoryLoaded){}
    else{
  if($('#trendingstories').visible()){
    $.fn.loadTrendingStory()
trendingStoryLoaded= true
  }
    }

    if(mostReadStoryLoaded){}
    else{
  if($('#mostreadstories').visible()){
    $.fn.loadMostReadStory()
mostReadStoryLoaded=true
  }
}

  if(interestStoriesLoaded){}
  else{
  if($('#intereststories').visible()){
    $.fn.loadInterestStory()
interestStoriesLoaded = true
  }
}

if(recommendedStoriesLoaded){}
else{
  if($('#recommendedstories').visible()){
    $.fn.loadRecommendedStory()
recommendedStoriesLoaded = true
  }

}
 

if(popularLibrariesLoaded){}
else{
if($('#popularlibraries').visible()){
    $.fn.loadPopularLibraries()
popularLibrariesLoaded = true
  }
}

}
)









{
    (function ($) {
        $('#search-input').on('input',function () {
            var query = $(this).val(); 
            if(query){
           $('#search-result').css('left','auto') 
          
            
            $('#search-result').empty()

            $.ajax({
                beforeSend: function () {
                                        
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url 'search_result' %}',
                data: {
                    'q' :query,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    if(data.empty){
                        
                    }
                    else{
                    $('#search-result').append(data.result_html);
                    }
                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });

        }});
    }(jQuery))
};

