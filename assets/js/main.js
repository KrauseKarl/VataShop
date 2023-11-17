/*
    Rex - Clean & Minimal Portfolio HTML5 Template
    Version: 1.0.1
    Author: Mountain-Themes
    Author URL: https://themeforest.net/user/mountain-themes
    Rex © 2023. Design & Coded by Mountain-Themes.
    
    TABLE OF CONTENTS
    ---------------------------
     1. Loading
     2. Mobile Menu
     3. Text animation
     4. Mini Cart
     5. Skillbars
     6. Counter
     7. LightCase
     8. Resize blocks
     9. Portfolio
     10. Wow
     11. Parallax
     12. Flex Slider
     13. Contact Form
     14. Header Sticky
     15. Google Map
*/


  jQuery.noConflict()(function ($) {

  'use strict';

  var isMobile = {
  Android: function () {
    return navigator.userAgent.match(/Android/i);
  },
  BlackBerry: function () {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  iPhone: function () {
    return navigator.userAgent.match(/iPhone/i);
  },
  iPad: function () {
    return navigator.userAgent.match(/iPad/i);
  },
  iPod: function () {
    return navigator.userAgent.match(/iPod/i);
  },
  iOS: function () {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
  },
  Opera: function () {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  Windows: function () {
    return navigator.userAgent.match(/IEMobile/i);
  },
  any: function () {
    return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
  }
  };

  /* ================================= */
  /* :::::::::: 1. Loading ::::::::::: */
  /* ================================= */

  $(document).ready(function () {

    mt_loading();
    mt_mobile_menu();
    mt_texteffect();
    mt_woo_minicart();
    mt_portfolio();
    mt_lightCase();
    mt_blogGrid();
    mt_shopGrid();
    mt_wow();
    mt_parallax();
    mt_flexslider();
    mt_ajax_contact_form();
    mt_skillbars_shortcode();
    mt_counter_shortcode();
    mt_google_map();
    mt_headerSticky();
    // extra
    extra_addItemCart();
    extra_chgItemCart();
    extra_delItemCart ();
    extra_sortItems();

  });

  // re-call functions for cube portfolio
  $(document).on('onAfterLoadMore.cbp', function(event) {
    mt_lightCase();
  });
  /* ================================= */
  /* :::::::::: 0.2 sort Items ::::::: */
  /* ================================= */
    function extra_sortItems() {
    $('a.shop-sort-button').on('click', function(event) {
        var sort_by = this.value;
        var dataString = 'sort_by='+ sort_by;
        alert(dataString)
        $.ajax({
            type: "GET",
            url: '/catalog-sort',
            data: dataString,
            success: function(data) {
                $("#catalog-item-list").html();

    //                    $("#catalog-item-list").load('/catalog #catalog-item-list > *#catalog-item-list');
            },
        });
        return false;
    });
    };

  /* ================================= */
  /* :::::::::: 0.3 toster ::::::::::: */
  /* ================================= */
    function toster(msg, color, imgItem) {
    $('.toast.fade').addClass('show');
    if(!imgItem) {
        if(color == 'toster__success') {
            var imgItem = '<i class="fa fa-check fa-lg" aria-hidden="true"></i>&ensp;'
            };
        if(color == 'toster__error') {
            var imgItem = '<i class="fa fa-exclamation-circle fa-lg" aria-hidden="true"></i>&ensp;'
            };
        if(color == 'toster__info') {
            var imgItem = '<i class="fa fa-trash-o fa-2x" aria-hidden="true"></i>&ensp;'
            };
    };
    $('.toast-body').html(imgItem+"&nbsp;"+msg).fadeIn('slow');
    $('.toast-body').addClass(color)
    setTimeout(function () {
        $('.toast-body').removeClass(color)
        $('.toast.fade').removeClass('show');
    }, 3000);
    };

  /* ================================= */
  /* :::::::::: 0.4 add Cart ::::::::: */
  /* ================================= */
    function extra_addItemCart() {
    $('.button-product').on("click", function() {
        event.preventDefault();
        var name = $('input#name').val();
        var quantity = $('input#quantity').val();
        var color = $('input#color').val();
        $.ajax({
            type: "POST",
            url: '/add',
            data: {'name': name, 'quantity': quantity,'color': color},
            success: function(data) {
                var count = data.item
                var cartPage = $( "#cart" );
                var product = data.product
                var totalSum = data.cart.total + '&#8381;'
                if(data.data == 'OK') {
                    var toasterMessage = product.title +" добавлен в корзину";
                    var toasterColor = "toster__success"
                    var imgAddItem = '<img src="' + data.img + '" class="m-1 p-1 rounded mr-2" width="50" alt="..."> '
                    var cartCount = '<i class="fa fa-shopping-bag" aria-hidden="true"></i><span class="cart-count"></span>'
                } else {
                    result = data;
                }

                $('.icon-cart').html(cartCount).fadeIn();
                $('.icon-cart-fix-bottom').html(cartCount).fadeIn();
                $('.fix__cart__total').html(totalSum).fadeIn();
                $('.cart-count').html(count).fadeIn();
                $(".cart-container").load("/cart_update")
                $('.icon-cart, .cart-widget').wrapAll('<div class="cart-container"></div>');
                toster(toasterMessage, toasterColor, imgAddItem);
          },
            error: function(data) {
                var toasterMessage = "Ошибка";
                var toasterColor = "toster__error";
                toster(toasterMessage, toasterColor);
            }
      });
        return false;
    });
    };

  /* ================================= */
  /* :::::::::: 0.4 change Cart :::::: */
  /* ================================= */
    function extra_chgItemCart() {
    // Quantity
    $(document).on('click', '.change-qty .plus, .change-qty .minus', function(event){
    event.preventDefault();
    var $this = $(this);

    var $qtty = $this.siblings('.qty');
    var item = $this.siblings('.hidden-name').val();

    var current = parseInt($qtty.val(), 10);
    var min = parseInt($qtty.attr('min'), 10);
    var max = parseInt($qtty.attr('max'), 10);
    var step = parseInt($qtty.attr('step'), 10);

    min = min ? min : 1;
    max = max ? max : current + step;

    if ($this.hasClass('minus') && current > min) {
    $qtty.val(current - step);
    $qtty.trigger('change');
    }
    if ($this.hasClass('plus') && current < max) {
    $qtty.val(current + step);
    $qtty.trigger('change');
    }
    var dataInsert = {'item_id': item, 'qty': $qtty.val()};
    console.log($qtty.val())
    $.ajax({
    type: "GET",
    url: '/cart-item-update',
    data: dataInsert,
    success: function(data) {
        if(data.status == 'OK') {
            var idd = '' + data.item_id;
            var count = data.count_items;
            if(data.extra == "removed"){
                var cardItem = "#item_" + data.removed_id
                var totalItem = "p#total_item_" + data.removed_id

                $('.cart span').html(count).fadeIn(1000);
                $(cardItem).remove().fadeOut(3000);
                $(totalItem).remove();
                var toasterMessage = 'Товар удален';
                var toasterColor = "toster__info";
                if(data.removed_all){
                    $("#container__total").remove().fadeOut(3000);
                    var emptyCart = "<div class='parallax' style='height:300px; margin-top:-50px;background-image: url(/assets/images/paralax/paralax_2.jpg)'><div class='info'><i style='text-shadow:2px 2px 4px rgb(0,0,0,0.4);' class='fa fa-shopping-cart fa-4x' aria-hidden='true'></i><h4 style='margin-top:20px;  text-shadow:2px 2px 7px rgb(0,0,0,0.4)'>Корзина пуста</h4></div></div>"
                    var emptyMiniCart = "<p class='mini-cart__total total'>корзина пуста</p>"
                    var emptyTotal = "<span class='fix__cart__total'>0&nbsp;&#8381;</span>"
                    $("#wrapper").html(emptyCart)
                    $(".cart-count").remove().fadeOut(3000);
                    $(".cart-widget").empty().html(emptyMiniCart)
                    $(".cart-count-fix-bottom").remove().fadeOut(3000);
                    $(".fix-bottom-total").remove().html(emptyTotal)
                }
            } else {
                var toasterMessage = 'Количество товара обновлено';
                var toasterColor = "toster__success";

                var quantity = "#" + idd + "_quantity";
                var summary = "#" + idd + "_summary";
                var totalSummary = "#" + idd + "__summary";

                $(quantity).text(data.cart['item'][idd]['quantity']).fadeIn(1000);
                $(summary).text(data.cart['item'][idd]['summary']).fadeIn(1000);
                $(totalSummary).text(data.cart['item'][idd]['summary']).fadeIn(1000);
                };
            $("#cart__total").text(data.cart["total"]).fadeIn(1000);
            } else {
                var cardItem = "#item_" + data.removed_id
                var totalItem = "p#total_item_" + data.removed_id
                console.log(totalItem)
                $('.cart span').html(count).fadeIn(1000);
                $(cardItem).remove().fadeOut(3000);
                $(totalItem).remove();
                var toasterMessage = 'Товар удален';
                var toasterColor = "toster__info";
                var imgAddItem = '<img src="' + data.img + '" class="m-1 p-1 rounded mr-2" width="75" alt="..."> '
            };
        toster(toasterMessage, toasterColor, imgAddItem);
        },
    error: function(data) {
                var toasterMessage = "Ошибка";
                var toasterColor = "toster__error";
                toster(toasterMessage, toasterColor);
            },
    });
    return false;
    });

    };

  /* ================================= */
  /* :::::::::: 0.4 remove Cart :::::: */
  /* ================================= */
    function extra_delItemCart () {
    $('.delete-button').on('click', function(event){
    event.preventDefault();
    var $this = $(this);
    var zeroQty = $this.siblings('.remove_qty');
    var zeroItem = $this.siblings('.remove_name').val();
    var dataInsert = {'item_id': zeroItem, 'qty': zeroQty.val()};
    $.ajax({
    type: "GET",
    url: '/cart-item-update',
    data: dataInsert,
    success: function(data) {
        if(data.status == 'OK') {
            var idd = '' + data.item_id;
            if(data.extra){
                var count = data.count_items
                var totalItem = "p#total_item_" + data.removed_id;
                var cardItem = "#item_" + data.removed_id;
                var cartCount = '<i class="fa fa-shopping-bag" aria-hidden="true"></i><span class="cart-count"></span>'
                var toasterMessage = "Товар удален";
                var toasterColor = "toster__error"
                $('.icon-cart').html(cartCount).fadeIn();
                $('.cart-count').html(count).fadeIn();
                $(cardItem).remove().fadeOut(3000);
                $(totalItem).remove();

                if(data.removed_all){

                    var emptyCart = "<div class='parallax' style='height:300px; margin-top:-50px;background-image: url(/assets/images/paralax/paralax_2.jpg)'><div class='info'><i style='text-shadow:2px 2px 4px rgb(0,0,0,0.4);' class='fa fa-shopping-cart fa-4x' aria-hidden='true'></i><h4 style='margin-top:20px;  text-shadow:2px 2px 7px rgb(0,0,0,0.4)'>Корзина пуста</h4></div></div>"
                    var emptyMiniCart = "<p class='mini-cart__total total'>корзина пуста</p>"
                    var emptyTotal = "<span class='fix__cart__total'>0&nbsp;&#8381;</span>"

                    $("#container__total").remove().fadeOut(3000);
                    $("#wrapper").html(emptyCart)
                    $(".cart-count").remove().fadeOut(3000);
                    $(".cart-widget").empty().html(emptyMiniCart)
                    $(".cart-count-fix-bottom").remove().fadeOut(3000);
                    $(".fix-bottom-total").remove().html(emptyTotal)
                }
            }
            $("#cart__total").text(data.cart["total"]).fadeIn(1000);
        } else {
            var toasterMessage = "Товар удален";
            var toasterColor = "toster__error";

        };
        var imgItem = '<img src="' + data.img + '" class="m-1 p-1 rounded mr-2" width="75" alt="..."> '
        toster(toasterMessage, toasterColor, imgItem);
        },
    error: function(data) {
                var toasterMessage = "Ошибка";
                var toasterColor = "toster__error";
                toster(toasterMessage, toasterColor);
            }
    });
    return false;
    });
    };

  /* ================================= */
  /* :::::::::: 1. Loading ::::::::::: */
  /* ================================= */
    function mt_loading() {
    $(".text-loader").delay(700).fadeOut();
    $(".page-loader").delay(900).fadeOut("fast");
    };

  /* ================================= */
  /* ::::::: 2. Mobile Menu :::::::::: */
  /* ================================= */

  function mt_mobile_menu() {

  $("#rex_menu").slicknav({
    prependTo: 'header .col-md-12',
    allowParentLinks: false
  });
  }

  /* ================================= */
  /* :::::: 3. Text animation :::::::: */
  /* ================================= */

  function mt_texteffect() {

  $(function () {
    $('.info h2').textillate();
  });
  }

  /* ================================= */
  /* ::::::::: 4. Mini Cart :::::::::: */
  /* ================================= */

  function mt_woo_minicart() {

    $('.icon-cart').on('click', function () {
      $('.cart-widget').toggleClass('widget-visible');
    });

    // Quantity
    $(document).on('click', '.shop-qtty .plus, .shop-qtty .minus', function(){
      var $this = $(this),
        $qty = $this.siblings('.qty'),
        current = parseInt($qty.val(), 10),
        min = parseInt($qty.attr('min'), 10),
        max = parseInt($qty.attr('max'), 10),
        step = parseInt($qty.attr('step'), 10);
        item = $this.siblings('.name'),

        console.log('item')
        console.log(item)

      min = min ? min : 1;
      max = max ? max : current + step;

      if ($this.hasClass('minus') && current > min) {
        $qty.val(current - step);
        $qty.trigger('change');
        console.log('minus')
      }

      if ($this.hasClass('plus') && current < max) {
        $qty.val(current + step);
        $qty.trigger('change');
        console.log('plus')
      }

      return false;
    });

  }

  /* ================================= */
  /* ::::::::: 5. Skillbars :::::::::: */
  /* ================================= */

  function mt_skillbars_shortcode() {

  $('.skillbar').appear(function () {
    var skillbar = $(this).html();
    $(this).skillBars({
      from: 0,
      speed: 3000,
      interval: 100,
      decimals: 0,
    });
  });
  }

  /* ================================= */
  /* :::::::::: 6. Counter ::::::::::: */
  /* ================================= */

  function mt_counter_shortcode() {

  $('.timer .number').appear(function () {
    var counter = $(this).html();
    $(this).countTo({
      from: 0,
      to: counter,
      speed: 3000,
      refreshInterval: 70
    });
  });
  }

  /* ================================= */
  /* :::::::: 7. LightCase ::::::::::: */
  /* ================================= */

  function mt_lightCase() {

  $('a.showcase').lightcase({
    transition: 'scrollVertical',
    speedIn: 400,
    speedOut: 300,
  });
  }

  /* ================================= */
  /* :::::: 8. Resize blocks ::::::::: */
  /* ================================= */

  function mt_blogGrid() {

  // Blog Grid
  var element = $('.blogContainer');
  element.imagesLoaded().done(function () {
    element.isotope({
      itemSelector: 'article',
      masonry: {
        columnWidth: 'article',
        gutter: '.gutter-sizer'
      },
      percentPosition: true
    });
  });
  $(window).on('blur change click dblclick error focus focusin focusout hover keydown keypress keyup load mousedown mouseenter mouseleave mousemove mouseout mouseover mouseup resize scroll select submit', function () {
    element.isotope();
    }
  ).trigger('resize');
  };

  function mt_shopGrid() {
  // Shop Grid
  var element = $('.shopContainer');
  element.imagesLoaded().done(function () {
    element.isotope({
      itemSelector: '.product',
      masonry: {
        columnWidth: '.product',
        gutter: '.gutter-sizer'
      },
      percentPosition: true
    });
  });
  $(window).on('blur change click dblclick error focus focusin focusout hover keydown keypress keyup load mousedown mouseenter mouseleave mousemove mouseout mouseover mouseup resize scroll select submit', function () {
    element.isotope();
  }).trigger('resize');
  }

  /* ================================= */
  /* ::::::::: 9. Portfolio :::::::::: */
  /* ================================= */

  function mt_portfolio() {

    $('.classicAnim').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 3,
    }, {
      width: 1100,
      cols: 3,
    }, {
      width: 800,
      cols: 2,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 15,
        gapVertical: 15,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 5,
    gapVertical: 5,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 200,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 3,
      }
    },
    });

    $('#grid-minimal').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 3,
    }, {
      width: 1100,
      cols: 3,
    }, {
      width: 800,
      cols: 2,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 15,
        gapVertical: 15,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 5,
    gapVertical: 5,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 100,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 3,
      }
    },
    });

    $('#grid-creative').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 3,
    }, {
      width: 1100,
      cols: 3,
    }, {
      width: 800,
      cols: 3,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 0,
        gapVertical: 0,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 0,
    gapVertical: 0,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 200,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 3,
      }
    },
    });

    $('#grid-alternative').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 3,
    }, {
      width: 1100,
      cols: 3,
    }, {
      width: 800,
      cols: 2,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 20,
        gapVertical: 20,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 30,
    gapVertical: 30,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 100,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 3,
      }
    },
    });

    $('#grid-shop').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'grid',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 3,
    }, {
      width: 1100,
      cols: 3,
    }, {
      width: 800,
      cols: 3,
    }, {
      width: 480,
      cols: 2,
    }, {
      width: 320,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 45,
        gapVertical: 35,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 45,
    gapVertical: 35,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 100,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 3,
      }
    },
    });

    $('#grid-blog').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 1,
    }, {
      width: 1100,
      cols: 1,
    }, {
      width: 800,
      cols: 1,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 40,
        gapVertical: 40,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 40,
    gapVertical: 40,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 100,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 2,
      }
    },
    });

    $('#grid-blogGrid').cubeportfolio({
    filters: '.portfolioFilter',
    layoutMode: 'masonry',
    sortByDimension: true,
    mediaQueries: [{
      width: 1500,
      cols: 2,
    }, {
      width: 1100,
      cols: 2,
    }, {
      width: 800,
      cols: 2,
    }, {
      width: 480,
      cols: 1,
      options: {
        caption: '',
        gapHorizontal: 40,
        gapVertical: 40,
      }
    }],
    defaultFilter: '*',
    animationType: 'quicksand',
    gapHorizontal: 40,
    gapVertical: 40,
    gridAdjustment: 'responsive',
    caption: 'zoom',
    displayType: 'sequentially',
    displayTypeSpeed: 100,

    plugins: {
      loadMore: {
        element: '.load-more',
        action: 'click',
        loadItems: 2,
      }
    },
    });

  }

  /* ================================= */
  /* :::::::::::: 10. Wow :::::::::::: */
  /* ================================= */

  function mt_wow() {
  new WOW().init();
  }

  /* ================================= */
  /* :::::::: 11. Parallax ::::::::::: */
  /* ================================= */

  function mt_parallax() {
  $('.parallax').jarallax({
    speed: 0.5,
    noAndroid: true
  });
  }

  /* ================================= */
  /* ::::::: 12. Flex Slider ::::::::: */
  /* ================================= */

  function mt_flexslider() {
  $('.flexslider').flexslider({
    controlNav: false,
    prevText: '<i class="fa fa-angle-left"></i>',
    nextText: '<i class="fa fa-angle-right"></i>',
    slideshowSpeed: '3000',
    pauseOnHover: true
  });
  }

  /* ================================= */
  /* :::::: 13. Contact Form ::::::::: */
  /* ================================= */

  function mt_ajax_contact_form() {

      $('#submit').on("click", function(event) {
            $('#submit').css("opacity","0.09");
            event.preventDefault();
            var name = $('input#name').val();
            var email = $('input#email').val();
            var phone = $('input#phone').val();
            var msg = $('textarea#msg').val();
            var dataDict = {"name": name, "email": email, "phone": phone, "msg": msg}
            $.ajax({
                type: "POST",
                url: "/send-order",
                data: dataDict,
                success: function(data) {
                      if(data.status == '200') {
                        var result = '<div class="notification_ok" style="font-weight:600;padding-bottom:20px;font-size:24px;height:381px;display:flex;justify-content:center;align-items:center;"><i class="fa fa-check fa-lg"></i> Заказ отправлен.</div>';
                        $("#ajax-order-form").find('input[type=text], input[type=email], textarea').val('');
                        $('#fields').css("opacity","1");
                        $('#submit').css("background-color","#000");
                      } else {
                      result = data;
                     }
                     $('#fields').html(result).fadeIn(3000);
                     setTimeout(function () {
                        $('#fields').html(result).fadeOut();
                     }, 4000);
                     setTimeout(function () {
                        window.location = data.url
                     }, 4000);
              }

            });
            return false;
           });

  };

  /* ================================= */
  /* :::::: 14. Header Sticky :::::::: */
  /* ================================= */

  function mt_headerSticky() {

if ($('header.sticky').length) {
$("header.sticky").sticky({ topSpacing: 0, zIndex: "99999" });

}

}

  /* ================================= */
  /* :::::::: 15. Google Map ::::::::: */
  /* ================================= */

  function mt_google_map() {

  if ($('#google-container').length) {
  //set your google maps parameters
  var latitude = -37.8602828,
    longitude = 145.079616,
    map_zoom = 10;
  //google map custom marker icon - .png fallback for IE11
  var is_internetExplorer11 = navigator.userAgent.toLowerCase().indexOf('trident') > -1;
  var marker_url = (is_internetExplorer11) ? 'assets/images/icon-location.png' : 'assets/images/icon-location.png';
  //define the basic color of your map, plus a value for saturation and brightness
  var main_color = '#2d313f',
    saturation_value = -70,
    brightness_value = 5;
  //we define here the style of the map
  var style = [{
    //set saturation for the labels on the map
    elementType: 'labels',
    stylers: [{
      saturation: saturation_value
    }, ]
  },
  { //poi stands for point of interest - don't show these lables on the map
    featureType: 'poi',
    elementType: 'labels',
    stylers: [{
      visibility: 'off'
    }, ]
  },
  {
    //don't show highways lables on the map
    featureType: 'road.highway',
    elementType: 'labels',
    stylers: [{
      visibility: 'off'
    }, ]
  },
  {
    //don't show local road lables on the map
    featureType: 'road.local',
    elementType: 'labels.icon',
    stylers: [{
      visibility: 'off'
    }, ]
  },
  {
    //don't show arterial road lables on the map
    featureType: 'road.arterial',
    elementType: 'labels.icon',
    stylers: [{
      visibility: 'off'
    }, ]
  },
  {
    //don't show road lables on the map
    featureType: 'road',
    elementType: 'geometry.stroke',
    stylers: [{
      visibility: 'off'
    }, ]
  },
  //style different elements on the map
  {
    featureType: 'transit',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'poi',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'poi.government',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'poi.attraction',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'poi.business',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'transit',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'transit.station',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'landscape',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]

  },
  {
    featureType: 'road',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry.fill',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{
        hue: main_color
      },
      {
        visibility: 'on'
      },
      {
        lightness: brightness_value
      },
      {
        saturation: saturation_value
      },
    ]
  }
];

//set google map options
var map_options = {
  center: new google.maps.LatLng(latitude, longitude),
  zoom: map_zoom,
  panControl: false,
  zoomControl: false,
  mapTypeControl: false,
  streetViewControl: false,
  mapTypeId: google.maps.MapTypeId.ROADMAP,
  scrollwheel: false,
  styles: style,
}

//inizialize the map
var map = new google.maps.Map(document.getElementById('google-container'), map_options);
//add a custom marker to the map

var marker = new google.maps.Marker({
  position: new google.maps.LatLng(latitude, longitude),
  map: map,
  title: 'Melbourne, Australia',
  visible: true,
  icon: marker_url,
});

google.maps.event.addDomListener(window, "resize", function () {
  var center = map.getCenter();
  google.maps.event.trigger(map, "resize");
  map.setCenter(center);

});

//add custom buttons for the zoom-in/zoom-out on the map
function CustomZoomControl(controlDiv, map) {
  //grap the zoom elements from the DOM and insert them in the map
  var controlUIzoomIn = document.getElementById('zoom-in'),
    controlUIzoomOut = document.getElementById('zoom-out');
  controlDiv.appendChild(controlUIzoomIn);
  controlDiv.appendChild(controlUIzoomOut);

  // Setup the click event listeners and zoom-in or out according to the clicked element
  google.maps.event.addDomListener(controlUIzoomIn, 'click', function () {
    map.setZoom(map.getZoom() + 1)
  });
  google.maps.event.addDomListener(controlUIzoomOut, 'click', function () {
    map.setZoom(map.getZoom() - 1)
  });
}

var zoomControlDiv = document.createElement('div');
var zoomControl = new CustomZoomControl(zoomControlDiv, map);

//insert the zoom div on the top left of the map
map.controls[google.maps.ControlPosition.LEFT_TOP].push(zoomControlDiv);
}
  }

  /* ================================= */
  /* :::::::: 16. ProductCard ::::::::: */
  /* ================================= */
   var ProductCard = function(){
    var $picts = $('.ProductCard-pict');
    var $photo = $('.ProductCard-photo');
    return {
        init: function(){
            $picts.on('click', function(e){
                e.preventDefault();



                var $this = $(this);
                var href = $this.attr('href');

                var colorId = $this.attr('id');
                var optionId = "#color-option_"+colorId;
                var inputColor = $('#color')
                inputColor.val(colorId);


                $photo.empty();
                $photo.append('<img src="'+ href +'" />');
                $picts.removeClass('ProductCard-pict_ACTIVE color-chosen');
                $this.addClass('ProductCard-pict_ACTIVE color-chosen');
            });
        }
    };
};
        ProductCard().init();
});