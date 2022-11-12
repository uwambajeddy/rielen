const responsive = {
    0:{
        items:1
    },
    320: {
        items: 1
    },
    576: {
        items: 1
    },
    768: {
        items: 2
    },
    992: {
        items: 3
    },
    1200: {
        items: 4
    },
    1400: {
        items: 5
    }
}

$(document).ready(function () {



    // owl-crousel for blog
    $('.carousel_se_01_carousel').owlCarousel({
        loop: false,
        autoplay: false,
        dots: false,
        nav: true,
        responsive : {
            0:{
                items:1
            },
            334: {
                items: 1
            },
            540: {
                items: 2
            },
            840: {
                items: 3
            },
            1200: {
                items: 4
            },
            1400: {
                items: 5
            }
        }
    });

    // owl-crousel for top
    $('.carousel_se_02_carousel').owlCarousel({
        loop: true,
        autoplay: false,
        autoplayTimeout: 3000,
        dots: true,
        nav: true,
        responsive : {
            0: {
                items: 1
            },
            320: {
                items: 1
            },
            560: {
                items: 1
            },
            960: {
                items: 1
            },
        }
        
    });


    // click to scroll top
    $('.move-up .move-up-click').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })

    // AOS Instance
    AOS.init();

   
});


const background = document.querySelector(".popover-background");
const closeButton = document.querySelector(".popover-close");
const popover = document.querySelector(".popover-custom");
const popoverImages = document.querySelectorAll(".popover-image");

popoverImages.forEach(popoverImage =>{
popoverImage.addEventListener("click",()=>{
popover.style.display ="block";
});
})

closeButton.addEventListener("click",()=>{
return closePopover();
});
background.addEventListener("click",()=>{
return closePopover();
});

function closePopover(){
   return popover.style.display ="none";
}

//notifications

const iconsNotification = document.querySelector(".icons-notification");
const notification = document.querySelector(".notifications");
const closeNotification = document.querySelector(".close-notification");
const searchForm = document.querySelector(".search-form");

iconsNotification.addEventListener("click",()=>{
    notification.style.display="block";
})
closeNotification.addEventListener("click",()=>{
    notification.style.display="none";
})

/*----------scroll detector---------*/

let nav = document.querySelector(".second-nav");

document.addEventListener("scroll",()=>{
    if(window.scrollY > 50){
        nav.style.background = "black" ;
    }else{
        nav.style.background = "linear-gradient(rgb(21, 22, 23), rgba(255, 0, 0, 0))";
    }
})







function create() {
    let overlay1 = document.querySelector(".overlay");
    let createUpdate = document.querySelector(".create-modal");
    let closebutton1 = document.querySelector(".close-modal");
  
    let closeC = function () {
      createUpdate.classList.add("hidden");
      overlay1.classList.add("hidden");
    };
  
    let openC = function () {
      createUpdate.classList.remove("hidden");
      overlay1.classList.remove("hidden");
    };
    openC();
  
    closebutton1.addEventListener("click", closeC);
    overlay1.addEventListener("click", closeC);
  }

searchForm.addEventListener("click",(e)=>{
    e.preventDefault();

})

