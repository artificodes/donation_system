


function replyTimeCalculator(el,replyYear,replyMonth,replyDay,replyHour,replyMinutes,replySeconds){

    var today = new Date();
   var reply_date = new Date(replyYear,replyMonth,replyDay,replyHour+1,replyMinutes,replySeconds)
   var today_Time = today.getTime()
   var reply_Time = reply_date.getTime()
   var calc_date = (today_Time-reply_Time)/(86400000)
   var reply_days = Math.round(calc_date)
   var reply_Hour  = calc_date*24
   var reply_Minutes  =reply_Hour*60
      
if(calc_date <= 1){
       if(reply_Hour <= 1){
           if(reply_Minutes <1){
               document.getElementById(el).innerHTML = 'just now'
           }
           else{
       document.getElementById(el).innerHTML = String(Math.round(reply_Minutes)) + ' min'}
    }
   
    else {
       document.getElementById(el).innerHTML = String(Math.round(reply_Hour)) + ' hrs'
    }
   
   
   }
   
   
   else{
       if (reply_days < 2){
        document.getElementById(el).innerHTML = String(reply_days) + ' day'

       }
       else{
       document.getElementById(el).innerHTML = String(reply_days) + ' days'
   }
}
}






