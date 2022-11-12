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

    $('.blog-content-mv').mouseenter(function() {
        let idM = document.getElementById(this.id.toString())
        let vd = idM.childNodes[3].childNodes[1];
        vd.play();
        vd.preload = 'metadata';
    });

    $('.blog-content-mv').mouseleave(function() {
        let idM = document.getElementById(this.id.toString())
        let vd = idM.childNodes[3].childNodes[1];
        vd.pause();
    });



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
        autoplay: true,
        autoplayTimeout: 25000,
        dots: false,
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
        }, 600);
        return false;
    }) 

    // AOS Instance
    /* AOS.init(); */

   
});


//notifications

const iconsNotification = document.querySelector(".icons-notification");
const notification = document.querySelector(".notifications-n");
const closeNotification = document.querySelector(".close-notification");
//const searchForm = document.querySelector(".search-form");
const close_sentAB = document.querySelector("#close_sentAB");

function notificationOpenF(){
    notification.style.display="block";
}

close_sentAB.addEventListener("click",()=>{
    document.querySelector("#sentAB").classList.add("hidden");
    document.querySelector(".overlay").classList.add("hidden");
})

iconsNotification.addEventListener("click",()=>{
    notificationOpenF()
})

function closeNotificationFun(){
    notification.style.display="none";
}

closeNotification.addEventListener("click",()=>{
    closeNotificationFun()
})

/*----------scroll detector---------*/

let nav = document.querySelector(".second-nav");
let mobileC = document.querySelector(".mobileC");
let tBtnNav = document.querySelector("#tBtnNav");

tBtnNav.addEventListener('click', ()=>{
    nav.style.background = "#161618" ;
    mobileC.style.background = "rgba(21, 22, 23, .9)" ;
    mobileC.classList.toggle('show')
})

document.addEventListener("scroll",()=>{
    if(window.scrollY > 50){
        nav.style.background = "#161618" ;
        mobileC.style.background = "rgba(21, 22, 23, .9)" ;
    }else{
        nav.style.background = "linear-gradient(rgb(21, 22, 23), rgba(255, 0, 0, 0))";
        mobileC.style.background = "";
    }
})




function specialClose(){
    let overlay1 = document.querySelector(".overlay");
    let createUpdate = document.querySelector(".create-modal");
    let createUpdates = document.querySelector("#signup_modal");
    overlay1.classList.add("hidden");
    createUpdate.classList.add("hidden");
    createUpdates.classList.add("hidden");
}


function loginBox() {
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

function signupBox() {
    let overlay1 = document.querySelector(".overlay");
    let createUpdate = document.querySelector("#signup_modal");
    let closebutton1 = document.querySelector("#signupC_modal");
  
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



const background = document.querySelector(".popover-background");
const closeButton = document.querySelector(".popover-close");
const popover = document.querySelector(".popover-custom");
const popoverImages = document.querySelectorAll(".popover-image");
const popover_dropDet = document.querySelector(".popover-dropDet");
const popover_details_mv = document.querySelector(".popover-details-mv");



const popover_loadingmv = document.querySelector(".popover-loading-mv");
const popover_containermv = document.querySelector(".popover-container-mv");


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
    popover.style.display ="none";
    popover_loadingmv.style.display ="block";
    popover_containermv.style.display ="none";
}

popover_dropDet.addEventListener('click', ()=>{
    popover_details_mv.classList.toggle('down');
    popover_dropDet.classList.toggle('down');
});


const urll = 'https://rielen.herokuapp.com/'
/* const urll = 'http://127.0.0.1:5000/' */


let p_video = document.querySelector(".popover-video video")
let popover_title = document.querySelector(".popover-title h2")
let popover_titlep = document.querySelector(".popover-title p")

let popover_content = document.querySelector(".popover-content h4")

let popover_dir = document.querySelector(".popover_dir")
let popover_cast = document.querySelector(".popover_cast")
let popover_writer = document.querySelector(".popover_writer")
let gernesBp = document.querySelector("#gernesBp")
let popover_loading_text = document.querySelector(".popover-loading-text")
let popover_loading_textImg = document.querySelector(".popover-loading-mv img")
let customerPwatchlater = document.querySelector("#customerPwatchlater")
let customerPWatchN = document.querySelector("#customerPWatchN")

function checkPOPmylistMv(id){
    $.ajax({
        
        url: urll+'resMvInMylist/'+id,
        method: 'GET',
        dataType: 'json',
        success: (data, status, xhr)=>{
            customerPwatchlater.children[0].classList = ''
            if (data['mssg'] == true){
                customerPwatchlater.classList.add('del')
                customerPwatchlater.children[0].classList.add('fas', 'fa-minus');
            }else{
                customerPwatchlater.classList.remove('del')
                customerPwatchlater.children[0].classList.add('fas', 'fa-plus');
            }
        }
    });
}

function addMylistPop(div, id){

    let f = document.querySelectorAll('.'+div)
    $.ajax({

        url: url+'mylist',
        method: 'POST',
        data: {'movieId': id},
        dataType: 'json',
        success: (data, status, xhr)=>{
            customerPwatchlater.children[0].className = '';
            if(data['action'] == 'post'){
                customerPwatchlater.classList.add('del');
                customerPwatchlater.children[0].classList.add('fas', 'fa-minus');

                f.forEach(p=>{
                    p.children[0].className = '';
                    p.classList.add('del')
                    p.children[0].classList.add('fas', 'fa-minus');
                });
                
                
            }else{
                
                customerPwatchlater.classList.remove('del');
                customerPwatchlater.children[0].classList.add('fas', 'fa-plus');

                f.forEach(p=>{
                    p.children[0].className = '';
                    p.classList.remove('del')
                    p.children[0].classList.add('fas', 'fa-plus');
                });
            }

        }


    });
}

function getseminame(id){
    $.ajax({
        
        url: urll+'getseminame/'+id,
        method: 'GET',
        dataType: 'json',
        success: (data, status, xhr)=>{
            customerPwatchlater.setAttribute('onclick', "addMylistPop('"+data['data']+"', '"+id+"')");
        }
    });
}

function settimeIntForTrailerDet(){
    setTimeout(()=>{
        popover_details_mv.classList.toggle('down');
        popover_dropDet.classList.toggle('down');
    }, 2000);
}

function customerPlayerTrailer(id, userIn){
    popover_loadingmv.style.visibility ="visible";
    popover_containermv.style.display ="none";
    popover.style.display ="block";
    customerPwatchlater.style.display ="block";
    popover_details_mv.classList.remove('down');
    popover_dropDet.classList.remove('down');
    
    
    $.ajax({
        
        url: urll+'api/v1/movie/'+id,
        method: 'GET',
        dataType: 'json',
        success: (data, status, xhr)=>{

            p_video.src = data['data'][0]['trailer']
            popover_title.innerHTML = data['data'][0]['movieTitle'];
            popover_titlep.innerHTML = data['data'][0]['smallTitle'];
            popover_content.innerHTML = data['data'][0]['Description'];
            popover_dir.innerHTML = data['data'][0]['director'];
            popover_cast.innerHTML = data['data'][0]['cast'];
            popover_writer.innerHTML = data['data'][0]['writter'];
            p_video.play()
            if(userIn == 'True'){
                checkPOPmylistMv(id)
                getseminame(id)
                customerPWatchN.href = '/watch/'+id;
            }

            popover_loadingmv.style.visibility = "hidden";
            popover_containermv.style.display = "block";

            gernesPv(data['data'][0]['gernes']);
            settimeIntForTrailerDet()
        },
        error: ()=>{
            popover_loading_text.innerHTML = 'Something went wrong, please close this and try again';
            popover_loading_textImg.style.display = 'none';
        }


    });
}
function customerPlayerTrailers(id){
    popover_loadingmv.style.visibility ="visible";
    popover_containermv.style.display ="none";
    popover.style.display ="block";
    customerPwatchlater.style.display ="none";
    popover_details_mv.classList.remove('down');
    popover_dropDet.classList.remove('down');
    
    
    $.ajax({
        
        url: urll+'api/v1/smovie/'+id,
        method: 'GET',
        dataType: 'json',
        success: (data, status, xhr)=>{

            p_video.src = data['data'][0]['trailer']
            popover_title.innerHTML = data['data'][0]['title'];
            popover_titlep.innerHTML = data['data'][0]['smallTitle'];
            popover_content.innerHTML = data['data'][0]['description'];
            popover_dir.innerHTML = data['data'][0]['director'];
            popover_cast.innerHTML = data['data'][0]['cast'];
            popover_writer.innerHTML = data['data'][0]['writter'];
            customerPWatchN.href = '/watch/shortmovie/'+id;
            
            popover_loadingmv.style.visibility = "hidden";
            popover_containermv.style.display = "block";

            gernesPvsm(data['data'][0]['gernes']);
            settimeIntForTrailerDet();
        },
        error: ()=>{
            popover_loading_text.innerHTML = 'Something went wrong, please close this and try again';
            popover_loading_textImg.style.display = 'none';
        }


    });
}

function closePopover(){
    popover.style.display ="none";
    p_video.src = 
    popover_containermv.style.display ="none";
    popover_loading_text.innerHTML = 'Loading';
            popover_loading_textImg.style.display = 'block';
}

function gernesPv(arr){

    gernesBp.innerHTML = ''

    arr.forEach((e)=>{
        let li = document.createElement('p');
        let a = document.createElement('a')
        a.textContent = e;
        a.href = '/movie?genre='+e;
        a.style.color = 'white';
        li.appendChild(a);
        gernesBp.appendChild(li);
    })

}

function gernesPvsm(arr){

    gernesBp.innerHTML = ''

    arr.forEach((e)=>{
        let li = document.createElement('p');
        let a = document.createElement('a')
        a.textContent = e;
        a.href = '/shortmovie?genre='+e;
        a.style.color = 'white';
        li.appendChild(a);
        gernesBp.appendChild(li);
    })

}