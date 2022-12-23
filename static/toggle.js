const togglePasswordButton = document.getElementById("toggle-password");
const password = document.getElementById("password");
const closedEyeIcon = document.querySelector("#closed-eye");
const openEyeIcon = document.querySelector("#open-eye");
const passwordElement = document.querySelector("#password");
let isPasswordVisible = true;

password.addEventListener("focusin", function(){
  togglePasswordButton.classList.add("color");
});

password.addEventListener("focusout", function(){
  togglePasswordButton.classList.remove("color");
});

togglePasswordButton.addEventListener("click", function(){
  password.focus();
  if (isPasswordVisible) {
    passwordElement.type = "text";
    closedEyeIcon.classList.add('hide');
    openEyeIcon.classList.remove('hide');
  }
  else {
    passwordElement.type = "password";
    closedEyeIcon.classList.remove('hide');
    openEyeIcon.classList.add('hide');
  }
  isPasswordVisible =! isPasswordVisible
});