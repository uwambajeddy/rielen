const RbtnM = document.querySelector(".RbtnM");
const Rmenu = document.querySelector(".Rmenu");
const Rcontent = document.querySelector(".Rcontent");
const RbtnImg = document.querySelector(".RbtnImg");



RbtnM.addEventListener("click",()=>{
    if (RbtnM.classList.contains('Rbtnl')){
        RbtnM.classList.remove('Rbtnl');
        Rmenu.classList.remove('RMF');
        Rcontent.classList.remove('RC');
        RbtnImg.src = '../static/icons/icons8-right-30.png';
    }else{
        RbtnImg.src = '../static/icons/icons8-left-30.png';
        RbtnM.classList.add('Rbtnl');
        Rmenu.classList.add('RMF');
        Rcontent.classList.add('RC');
    }
});