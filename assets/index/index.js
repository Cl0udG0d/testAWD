function noticeUp(obj, top, time) {
    $(obj).animate({
        marginTop: top
    }, time, function() {
        $(this).css({ marginTop: "0" }).find(":first").appendTo(this);
    })
}