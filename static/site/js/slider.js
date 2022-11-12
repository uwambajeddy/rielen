$(document).ready(function() {

const category_slides = new Swiper('#category-slides', {
    // Optional parameters
    direction: 'horizontal',
    loop: false,

    breakpoints: {

        350:{
            slidesPerView: 'auto',
            spaceBetween: 4,
        },

        806: {
            slidesPerView: 'auto',
            spaceBetween: 3
        },

        1120: {
            slidesPerView: 'auto',
            spaceBetween: 3
        },

        1500: {
            slidesPerView: 'auto',
            spaceBetween: 5
        },

        1920: {
            slidesPerView: 'auto',
            spaceBetween: 4
        },

        2880: {
            slidesPerView: 'auto',
            spaceBetween: 6
        }
        
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.slides-btns-move.right-btn',
      prevEl: '.slides-btns-move.left-btn',
    },
  });

});