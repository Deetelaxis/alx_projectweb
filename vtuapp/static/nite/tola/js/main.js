/*----------------------

    Template Name: Gethost Htlml template
    Template URI: http://hastech.company/
    Description: This is html5 template
    Author: Hastech
    Author URI: http://hastech.company/
    Version: 1.0
---------------------------*/
(function ($) {
  "use strict";

  /*-------------------------------------------
     jQuery MeanMenu
  --------------------------------------------- */
  jQuery('nav#dropdown').meanmenu();

  /*-------------------------------------------
     wow js active
  --------------------------------------------- */
  new WOW().init();

  /*----------------------------
     stickey menu
  ----------------------------*/
  $(window).on('scroll', function () {
    var scroll = $(window).scrollTop();
    if (scroll < 265) {
      $(".sticky-header").removeClass("sticky");
    } else {
      $(".sticky-header").addClass("sticky");
    }
  });

  /*--
  menu-toggle
  ------------------------*/
  $('.menu-toggle').on('click', function () {
    if ($('.menu-toggle').hasClass('is-active')) {
      $('.menu-js nav').removeClass('menu-open');
    } else {
      $('.menu-js nav').addClass('menu-open');
    }
  });

  /*--
          Hamburger js
      -----------------------------------*/
  var forEach = function (t, o, r) { if ("[object Object]" === Object.prototype.toString.call(t)) for (var c in t) Object.prototype.hasOwnProperty.call(t, c) && o.call(r, t[c], c, t); else for (var e = 0, l = t.length; l > e; e++)o.call(r, t[e], e, t) };

  var hamburgers = document.querySelectorAll(".hamburger");
  if (hamburgers.length > 0) {
    forEach(hamburgers, function (hamburger) {
      hamburger.addEventListener("click", function () {
        this.classList.toggle("is-active");
      }, false);
    });
  }
  /*-------------------------
     Gethost slider
    ------------------------------ */

  $(".slider-list").owlCarousel({
    autoPlay: false,
    slideSpeed: 2000,
    pagination: false,
    navigation: true,
    items: 1,
    transitionStyle: "fade",     /* [This code for animation ] */
    navigationText: ["<i class='icofont icofont-arrow-left'></i>", "<i class='icofont icofont-arrow-right''></i>"],
    itemsDesktop: [1199, 1],
    itemsDesktopSmall: [980, 1],
    itemsTablet: [768, 1],
    itemsMobile: [479, 1],
  });


  $(".testimonial-list").owlCarousel({
    autoPlay: false,
    slideSpeed: 2000,
    pagination: true,
    navigation: false,
    items: 1,
    itemsDesktop: [1199, 1],
    itemsDesktopSmall: [980, 1],
    itemsTablet: [768, 1],
    itemsMobile: [479, 1],
  });

  $(".testimonial-list-2").owlCarousel({
    autoPlay: false,
    slideSpeed: 2000,
    pagination: true,
    navigation: false,
    items: 3,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [980, 2],
    itemsTablet: [768, 2],
    itemsTablet: [767, 1],
    itemsMobile: [479, 1],
  });

  $(".brand-list-2").owlCarousel({
    autoPlay: false,
    slideSpeed: 2000,
    pagination: false,
    navigation: false,
    items: 5,
    itemsDesktop: [1199, 5],
    itemsDesktopSmall: [980, 4],
    itemsTablet: [768, 2],
    itemsMobile: [479, 1],
  });


  /*--------------------------
      Counter Up
  ---------------------------- */
  $('.counter').counterUp({
    delay: 70,
    time: 5000
  });
  /*--------------------
    Accordion
  -------------------------*/
  $(".faq-accordion").collapse({
    accordion: true,
    open: function () {
      this.slideDown(550);
    },
    close: function () {
      this.slideUp(550);
    }
  });
  /*------magnificPopup js-----*/
  $('.post-video-play > a').magnificPopup({
    disableOn: 0,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: true,

    fixedContentPos: false
  });
  /*--
   team slider js
  -----------------------------------*/
  $('.team-slider-active').slick({
    centerMode: true,
    centerPadding: '0',
    slidesToShow: 3,
    prevArrow: '<button class="slick-prev ss2-prev" type="button"><i class="icofont icofont-arrow-left"></i></button>',
    nextArrow: '<button class="slick-next ss2-next" type="button"><i class="icofont icofont-arrow-right"></i></button>',
    asNavFor: '.team-text-slider'
  });

  $('.team-text-slider').slick({
    slidesToShow: 1,
    arrows: false,
    asNavFor: '.team-slider-active'
  });

  /*--
   isotope js
  -----------------------------------*/


  $('.blog-post-list').imagesLoaded(function () {
    $('.blog-post-list').isotope({
      itemSelector: '.blog-post',
      percentPosition: true,
      masonry: {
        // use outer width of grid-sizer for columnWidth
        columnWidth: '.blog-post'
      }
    })
  });


  /*-------------------------------------------
    scrollUp jquery active
  --------------------------------------------- */
  $.scrollUp({
    scrollText: '<i class="icofont icofont-simple-up"></i>',
    easingType: 'linear',
    scrollSpeed: 900,
    animation: 'fade'
  });

  $('select').niceSelect();


})
  (jQuery);




