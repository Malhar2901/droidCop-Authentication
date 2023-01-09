
let element = document.querySelector("#element");
let again = document.querySelector("#again");
let cloud = document.querySelector("#cloud");
let startbutton = document.querySelector('#startbutton');
let dp = document.querySelector('#dp');
let tooltip = document.querySelector('#tooltip');
let record = document.querySelector('#rec');
element.removeChild(cloud)
element.removeChild(again)
element.removeChild(record)

tooltip.addEventListener('click', logout_user)
dp.addEventListener('click', showlogout)
function showlogout(){
 
  if(tooltip.style.opacity=="1"){
    tooltip.style.opacity = "0";
    dp.classList.add("dpbutton")
dp.classList.remove("dpbuttonclick")
  } 
 else{
    tooltip.style.opacity = "1";
    dp.classList.remove("dpbutton")
dp.classList.add("dpbuttonclick")
  }
 
}

startbutton.addEventListener('click', changeStuff)

function changeStuff(){
  
startbutton.classList.remove("bluebutton")
startbutton.classList.add("darkbutton")
startbutton.innerHTML="Stop Recording"
element.appendChild(record)
let stopbutton = startbutton;
stopbutton.addEventListener('click', twobuttons)
}


function twobuttons(){
  element.removeChild(startbutton)
  element.appendChild(again)
  element.appendChild(cloud)
  element.removeChild(record)
  again.addEventListener('click', startrecording)
}
function startrecording(){
  element.removeChild(again)
  element.removeChild(cloud)
  element.appendChild(record)
  element.appendChild(startbutton)
}

function logout_user(){
 fetch("http://127.0.0.1:5000/logout",{ method:'GET',redirect:'follow'}).then((res)=>{
 if (res.redirected){
 window.location.href=res.url
 }
 })


}
