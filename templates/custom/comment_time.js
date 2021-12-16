

{
    (function ($) { //Most read async
        $('#loadcomment').on('click', function () {
            


        });
    }(jQuery))
};


function commentTimeCalculator(el,commentYear,commentMonth,commentDay,commentHour,commentMinutes,commentSeconds){

    var today = new Date();
   var comment_date = new Date(commentYear,commentMonth,commentDay,commentHour+1,commentMinutes,commentSeconds)
   var today_Time = today.getTime()
   var comment_Time = comment_date.getTime()
   var calc_date = (today_Time-comment_Time)/(86400000)
   var comment_days = Math.round(calc_date)
   var comment_Hour  = calc_date*24
   var comment_Minutes  =comment_Hour*60
      
if(calc_date <= 1){
       if(comment_Hour <= 1){
           if(comment_Minutes <1){
               document.getElementById(el).innerHTML = 'just now'
           }
           else{
       document.getElementById(el).innerHTML = String(Math.round(comment_Minutes)) + ' min'}
    }
   
    else {
       document.getElementById(el).innerHTML = String(Math.round(comment_Hour)) + ' hrs'
    }
   
   
   }
   
   
   else{
       if(comment_days<2){
        document.getElementById(el).innerHTML = String(comment_days) + ' day'
      
       }
      else{ document.getElementById(el).innerHTML = String(comment_days) + ' days'}
   }
}






