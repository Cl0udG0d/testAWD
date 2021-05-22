

setInterval(
         function(){
             $.ajax({
                 type: "POST",
                 dataType: "json",
                 url: "/lastTime",//后端请求url地址
                 success: function (data) {
                 document.getElementById('lasttime').innerHTML = data.time;
                    console.log(data)
                 }
             })
         }, 100);

