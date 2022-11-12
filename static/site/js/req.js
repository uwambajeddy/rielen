/* const url = 'http://127.0.0.1:5000/' */
const url = 'https://rielen.herokuapp.com/'

$(document).ready(()=>{


    function emailSent(email, userid){
        let sentAB = document.querySelector("#sentAB");
        let loginBoxx = document.querySelector(".loginBoxx");
        let signup_modal = document.querySelector("#signup_modal");
        let confLinkHref = document.querySelector("#confLinkHref");
        let modal_hE_email = document.querySelector("#modal_hE_email");
        
        confLinkHref.href = url+'sendactivationlink?token='+userid;
        modal_hE_email.innerHTML = '(Email: '+email+')';

        sentAB.classList.remove("hidden");
        loginBoxx.classList.add("hidden");
        signup_modal.classList.add("hidden");
    }

    let notInp = document.querySelector(".notInp");
    let notInp_p = document.querySelector(".notInp_p");
    let notInpp = document.querySelector(".notInpp");
    let notInp_pp = document.querySelector(".notInpp_p");

    document.querySelector(".notInpCloseBtn").addEventListener('click', ()=>{
        notInp.classList.add('Nhidden');
    });
    
    function notInpF(color, mssg){

        notInp.classList.remove('Nhidden');

        if(color == 'red'){
            notInp.style.borderColor='red'; 
            notInp.style.backgroundColor  = 'rgba(255, 0, 0, .1)'; 
        }else{
            notInp.style.borderColor = '#008000'; 
            notInp.style.backgroundColor  = 'rgba(0, 128, 0, .1)'; 
        }
        notInp_p.innerHTML = mssg;
    }

    document.querySelector(".notInpCloseBtnp").addEventListener('click', ()=>{
        notInp.classList.add('Nhidden');
    });
    
    function notInpFp(color, mssg){

        notInpp.classList.remove('Nhidden');

        if(color == 'red'){
            notInpp.style.borderColor='red'; 
            notInpp.style.backgroundColor  = 'rgba(255, 0, 0, .1)'; 
        }else{
            notInpp.style.borderColor = '#008000'; 
            notInpp.style.backgroundColor  = 'rgba(0, 128, 0, .1)'; 
        }
        notInp_pp.innerHTML = mssg;
    }


    // Login Process
    $( "#loginForm" ).submit(function( event ) {

        event.preventDefault();
        let logname= $('input[name="logname"]').val();
        let password= $('input[name="password"]').val();
        let urlR = $('input[name="url"]').val();
        let loginformBox = document.querySelector("#loginformBox");

        console.log(url)


        
        if (!navigator.cookieEnabled) {
            alert('The browser does not support or is blocking cookies from being set., we wont be able to set cookies to your browser in this login process')
        }else{

            loginformBox.disabled = true;
            loginformBox.innerHTML = '<img src="../static/site/gif/30.gif" width="80px" alt="">';
            
            $.ajax({

                url: url+'login',
                method: 'POST',
                data: {'logname': logname, 'password': password, 'url': urlR},
                dataType: 'json',
                success: (data, status, xhr)=>{
                    
                    if(data["message"] == "sent activation link"){
                        notInpF('green', data["message"]);
                        emailSent(data["data"]["email"], data["data"]['userId']);
                        loginformBox.innerHTML = 'Login';
                        loginformBox.disabled = false;
                    }

                    if(data["message"] == "login successful"){
                        notInpF('green', data["message"]);
                        window.location.href = data['url'];
                    }
                     

                },

                error: function (jqXhr, textStatus, errorMessage) {
                    mssg = JSON.parse(jqXhr.responseText)
                    notInpF('red', mssg["message"]);

                    loginformBox.innerHTML = 'Login';
                    loginformBox.disabled = false; 
                }


            });
        }

      });



    // Signup Process
    $( "#signup_modal" ).submit(function( event ) {

        event.preventDefault();
        let firstname= $('input[name="firstname"]').val()
        let lastname= $('input[name="lastname"]').val()
        let email= $('input[name="email"]').val()
        let username= $('input[name="username"]').val()
        let password= $('input[name="spassword"]').val()
        let cpassword= $('input[name="cpassword"]').val()
        let gender= $('input[name="gender"]').val()
        let phonenumber= $('input[name="phonenumber"]').val()
        let signupformBox = document.querySelector("#signupformBox");


        if (!navigator.cookieEnabled) {
            alert('The browser does not support or is blocking cookies from being set., we wont be able to set cookies to your browser in this Signup process')
        }else{


            signupformBox.disabled = true; 
            signupformBox.innerHTML = '<img src="../static/site/gif/30.gif" width="80px" alt="">';

            $.ajax({

                url: url+'register',
                method: 'POST',
                data: {'firstname': firstname, 'lastname': lastname, 'email': email, 'username': username, 'password': password, 'cpassword': cpassword, 'gender': gender, 'phonenumber': phonenumber},
                dataType: 'json',
                success: (data, status, xhr)=>{
                
                    notInpFp('green', data["message"]);
                    emailSent(data["data"]["email"], data["data"]['userId']);

                    signupformBox.innerHTML = 'Signup';
                    signupformBox.disabled = false; 

                },

                error: function (jqXhr, textStatus, errorMessage) {
                    mssg = JSON.parse(jqXhr.responseText)
                    notInpFp('red', mssg["message"]);
                    signupformBox.innerHTML = 'Signup';
                    signupformBox.disabled = false; 
                }


            });
        }

      });
})

function mylist(e, id){


    $.ajax({

        url: url+'mylist',
        method: 'POST',
        data: {'movieId': id},
        dataType: 'json',
        success: (data, status, xhr)=>{
            let c = e.classList
            x = ''
            c.forEach(element => {
                if (element != 'button' && element != 'watchlater-button' && element != 'watchlater-button'){
                    x = element
                }
            });
            e.children[0].className = '';
            if(data['action'] == 'post'){
                e.classList.add('del');
                e.children[0].classList.add('fas', 'fa-minus');

                if(x !=''){
                    let f = document.querySelectorAll('.'+x);

                    f.forEach(p=>{
                        p.children[0].className = '';
                        p.classList.add('del')
                        p.children[0].classList.add('fas', 'fa-minus');
                    });
                }
                
                
            }else{
                
                e.classList.remove('del');
                e.children[0].classList.add('fas', 'fa-plus');

                if(x !=''){
                    let f = document.querySelectorAll('.'+x);

                    f.forEach(p=>{
                        p.children[0].className = '';
                        p.classList.remove('del')
                        p.children[0].classList.add('fas', 'fa-plus');
                    });
                }
            }

        }


    });
    
}

function removeMylist(e, id){
    $.ajax({

        url: url+'removemylist/'+id,
        method: 'DELETE',
        dataType: 'json',
        success: (data, status, xhr)=>{
            let elem = e.parentElement.parentElement.parentElement.parentElement
            elem.style.display = 'none'
        }


    });
}



/* Movie */

function getWLoc(){

    const getURL = window.location.search;
    const urlParams = new URLSearchParams(getURL);

    if (urlParams.has('genre')){
        genre = urlParams.get('genre')
    }else{
        genre = null
    }

    if (urlParams.has('sort')){
        sort = urlParams.get('sort')
    }else{
        sort = null
    }

    return [genre, sort]
}

function changeSort(e){
    val = e.value
    d = getWLoc()

    if (d[0] != null){

        newURL = url+'movie?genre='+d[0]+'&sort='+val
        
    }else{
        
        newURL = url+'movie?sort='+val

    }

    window.location.href = newURL
}

function changeGenreC(e){
    val = e.value
    d = getWLoc()

    if (d[1] != null){

        newURL = url+'movie?genre='+val+'&sort='+d[1]
        
    }else{
        
        newURL = url+'movie?genre='+val

    }

    window.location.href = newURL
}
function changeSortS(e){
    val = e.value
    d = getWLoc()

    if (d[0] != null){

        newURL = url+'shortmovie?genre='+d[0]+'&sort='+val
        
    }else{
        
        newURL = url+'shortmovie?sort='+val

    }

    window.location.href = newURL
}

function changeGenreCS(e){
    val = e.value
    d = getWLoc()

    if (d[1] != null){

        newURL = url+'shortmovie?genre='+val+'&sort='+d[1]
        
    }else{
        
        newURL = url+'shortmovie?genre='+val

    }

    window.location.href = newURL
}

function behindSceneClick(e){
    window.location.href = url+'behindscene?id='+e
}

function documentaryClick(e){
    window.location.href = url+'documentary?id='+e
}



  
/* ---------------------- */