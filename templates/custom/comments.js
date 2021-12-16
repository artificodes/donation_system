

var most_read_comments_array = []
var trending_comments_array = []
var trending_comments = []
var inline_loader = "{% include 'custom/inline_loading.html' %}"
var recommended_inline_loader = "{% include 'custom/recommended_inline_loading.html' %}"
var inline_loader_small_center = "{% include 'custom/inline_loading_small_center.html' %}"

function showCommentBox(commentbtn,el,){
   document.getElementById(commentbtn).setAttribute('onclick','hideCommentBox("'+commentbtn+'","'+el+'")')
                         document.getElementById(el).style.animationDuration ='0.5s'
document.getElementById(el).style.animationName='uk-fade-top'
document.getElementById(el).style.display ='block'
 document.getElementById(el).style.display ='block'
 document.getElementById(commentbtn).style.display ='block'

 }

function foldCommentBox(el,foldcomment,unfoldcont){
    document.getElementById(foldcomment).style.display='none'

   document.getElementById(el).style.animationName='c-fade-top'
   document.getElementById(el).style.animationDuration='0.5s'
document.getElementById(unfoldcont).style.display='block'
function hideElement(){
document.getElementById(el).style.display='none'
}
   setTimeout(hideElement,500)

}

function unfoldCommentBox(el,unfoldbtn,foldbtn){
    document.getElementById(foldbtn).style.display='inline'

    document.getElementById(el).style.animationName='c-fade-bottom'
    document.getElementById(el).style.animationDuration='0.5s'
    document.getElementById(unfoldbtn).style.display='none'

 document.getElementById(el).style.display='block'
}

function foldReplyBox(el,unfoldbtn,foldbtn){
    var foldbtns = document.getElementsByClassName(foldbtn)
    for(let i = 0;i<foldbtns.length;i++){
            foldbtns[i].style.display='none'
    }

   document.getElementById(el).style.animationName='c-fade-top'
   document.getElementById(el).style.animationDuration='0.5s'
document.getElementById(unfoldbtn).style.display='inline'
function hideElement(){
document.getElementById(el).style.display='none'
}
   setTimeout(hideElement,500)

}


function unFoldReplyBox(el,unfoldbtn,foldbtn){
    var foldbtns = document.getElementsByClassName(foldbtn)
    for(let i = 0;i<foldbtns.length;i++){
            foldbtns[i].style.display='inline'
    }
    document.getElementById(el).style.animationName='c-fade-bottom'
    document.getElementById(el).style.animationDuration='0.5s'
    document.getElementById(unfoldbtn).style.display='none'

 document.getElementById(el).style.display='block'
}




 function hideCommentBox(commentbtn,el){
           document.getElementById(commentbtn).setAttribute('onclick','showCommentBox("'+ commentbtn+'","'+el+'")')
document.getElementById(el).style.display ='none'

}

var replyboxes =[]

    function showReplyBox(replybtn,el){
       replyboxes =  document.getElementsByClassName('replybox')
          for(let i =0;i<replyboxes.length;i++){
            replyboxes[i].style.display = 'none'
          }
              document.getElementById(replybtn).setAttribute('onclick','hideReplyBox("'+replybtn+'","'+el+'")')
                            document.getElementById(el).style.animationDuration ='0.5s'
document.getElementById(el).style.animationName='uk-fade-top'

  
        document.getElementById(el).style.display ='block'

    }

    function hideReplyBox(replybtn,el){
              document.getElementById(replybtn).setAttribute('onclick','showReplyBox("'+ replybtn+'","'+el+'")')
  document.getElementById(el).style.display ='none'

        

}

{% if episode.episode_id %}
{
    (function ($) { //Most read async
        $('.more-comments').on('click', function () {
            var link = $(this);
            var newcomments = link.data('page');
            
            $.ajax({
                beforeSend: function () {
                    
                    
                },
                complete: function () {

                },
                type: 'post',
                url: '{% url "comments" episode_id=episode.episode_id %}',
                data: {
                    'newcomments': newcomments,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN, // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    
                    // append html to the posts div

                    $('#commentscontainer').append(data.comments_html);
                    $('.csrf').val(window.CSRF_TOKEN)


                    $('#commentscontainerouter').css('display','block')
                    if (data.has_next) {
                        $('.more-comments').data('page', newcomments + 1);
                        
                    } else {
                        $('.more-comments').attr('class','disabled uk-icon-button uk-disabled')
                       $('#more-comments').css('display','none')
                    }

                },
                error: function (xhr, status, error) {
                    alert('there was an error')
                }
            });
        });
    }(jQuery))
};


{% endif %}

