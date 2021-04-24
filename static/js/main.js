(function($) {
  "use strict";

  $(window).on("load", function() {
    $(".loader").addClass("completein", 300);
    setTimeout(function() {
      $(".preloader").addClass("complete");
    }, 10);
  });

  jQuery(document).ready(function($) {
    /* \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                      Contact form ajax
        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ */
    var contactSubmit = $("#contact-submit");
    contactSubmit.on("click", function(e) {
      e.preventDefault();
      var name = $("#form-name").val();
      var email = $("#form-email").val();
      var message = $("#form-message").val();
      var form = new Array({
        name: name,
        email: email,
        message: message
      });
      $.ajax({
        type: "POST",
        url: "contact.php",
        data: {
          action: "contact",
          form: form
        }
      }).done(function(data) {
        var conResult = $("#result");
        conResult.html(data);
        $(".contact_form")[0].reset();
      });
    });

    // video popup //
    $(".youtube").colorbox({
      iframe: true,
      transition: "elastic",
      innerWidth: 640,
      innerHeight: 409,
      closeButton: false,
      maxWidth: "90%"
    });

    // Tooltip      //
    $('[data-toggle="tooltip"]').tooltip();

    /* \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                  Mega Menu
        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ */
    function checkWidth() {
      var windowsize = window.innerWidth;
      if (windowsize < 768) {
        $(".dropdown_content")
          .removeClass("collapse relative")
          .addClass("collapse relative");
      } else {
        $(".dropdown_content")
          .addClass("collapse relative")
          .removeClass("collapse relative");
      }
    }

    checkWidth();
    $(window).resize(checkWidth);

    // Testimonial Carousel
    var mySwiper = new Swiper(".testimonial_area .swiper-container", {
      direction: "horizontal",
      slidesPerView: 1,
      loop: true,
      centeredSlides: true,
      autoplay: {
        delay: 2000,
        disableOnInteraction: false
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true
      }
    });

    // Client Carousel
    var mySwiper = new Swiper(".client_area .swiper-container", {
      direction: "horizontal",
      slidesPerView: 5,
      // slidesPerView: 'auto',
      spaceBetween: 30,
      loop: true,
      centeredSlides: false,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false
      },
      breakpoints: {
        1200: {
          slidesPerView: 4,
          centeredSlides: false
        },
        992: {
          slidesPerView: 3,
          centeredSlides: false
        },
        768: {
          slidesPerView: 2,
          centeredSlides: false
        },
        480: {
          slidesPerView: 1,
          centeredSlides: false
        }
      }
    });

    /* \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                      Scroll to top
        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ */
    function topFunction() {
      $(".scrolltop").on("click", function() {
        $("html, body").animate({ scrollTop: 0 }, 200);
        return false;
      });
    }
    topFunction();
  });

  $(window).on("scroll", function() {
    /* \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                      Scroll to top 
        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ */
    var scroll = $(window).scrollTop();
    if (scroll >= 300) {
      setTimeout(function() {
        $(".scrolltop").addClass("is_scroll");
      }, 200);
    } else {
      setTimeout(function() {
        $(".scrolltop").removeClass("is_scroll");
      }, 200);
    }
  });
})(jQuery);
