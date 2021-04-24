$(function() {
        $('ol li').click(function() {
                // 页面平滑的滚动到相应的位置
                scrollToTop($("." + $(this).attr("id")).offset().top)
            })
            /* 监听滚动 */
        $(document).scroll(function() {
            if ($(document).height() <= (parseInt($(document).scrollTop() + 1) + $(window).height())) { //滚动条滑到底部啦
                $("ol li").removeClass('active')
                $("ol li:last").addClass('active')
                return;
            }
            var top = $(document).scrollTop(); //滚动条距离顶部的高度
            $(".text").each(function(i, item) {
                if ($(this).offset().top <= top) {
                    $("ol li").removeClass('active')
                    $("#" + item.classList[1]).addClass('active');
                }
            })
        });
    })
    /** 将滚动轴滚到相应位置 */
function scrollToTop(number) {
    window.scrollTo({
        top: number,
        behavior: "smooth"
    });
}