$(function(){

    var btn_cc = 'btn-primary';
    var navbar_cc = 'cm-navbar-primary';


    $('#demo-buttons button').click(function(){
	var color = $(this).data('switch-color');
	$('.cm-navbar').removeClass(navbar_cc);
	navbar_cc = 'cm-navbar-' + color;
	$('.cm-navbar').addClass(navbar_cc);
	$('.cm-navbar .btn').removeClass(btn_cc);
	btn_cc = 'btn-' + color;
	$('.cm-navbar .btn').addClass(btn_cc);
    });














});
