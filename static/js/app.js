setInterval(
         function(){
             $.ajax({
                 type: "POST",
                 dataType: "json",
                 url: "/currentRound",//后端请求url地址
                 success: function (data) {
                 document.getElementById('currentRound').innerHTML = data.time;
                    console.log(data)
                 }
             })
         }, 1000);
var doStuff = function () {
    $.ajax({
                 type: "POST",
                 dataType: "json",
                 url: "/currentSource",//后端请求url地址
                 success: function (data) {
                 document.getElementById('currentSource').innerHTML = data.source;
                    console.log(data)
                 }
             })
    setTimeout(doStuff, 10000);
}
doStuff();
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

//tab切换
    $('.tab-button').click(function() {
        var tab = $(this).data('tab')
        $(this).addClass('cur').siblings('.tab-button').removeClass('cur');
        $('#tab-' + tab + '').addClass('active').siblings('.tab-item').removeClass('active');
    }
    );
    //新闻列表切换
    $('.information-tab .article-list').hover(function() {
        $(this).addClass('current').siblings('.article-list').removeClass('current');
    }

    ,function() {
        $(this).parent('.information-right').find('.article-list:first-of-type').addClass('current').siblings('.article-list').removeClass('current');
    }
    );