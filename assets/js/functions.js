function learningDropdown() {
  document.querySelector(".learning-dropdown-hidden-box").classList.toggle("learning-dropdown-box");
  document.querySelector(".learning-menu-heading-inactive").classList.toggle("learning-menu-heading-active");
  document.querySelector(".drp-down-btn1").classList.toggle("drp-down-btn-flipped");
  if (document.querySelector(".challenge-dropdown-box")) {
    challengeDropdown()
    
  }
  if (document.querySelector(".opportunities-dropdown-box")) {
    opportunitiesDropdown()
  }
}

function challengeDropdown() {
  document.querySelector(".challenge-dropdown-hidden-box").classList.toggle("challenge-dropdown-box");
  document.querySelector(".challenge-menu-heading-inactive").classList.toggle("challenge-menu-heading-active");
  document.querySelector(".drp-down-btn2").classList.toggle("drp-down-btn-flipped");
  if (document.querySelector(".learning-dropdown-box")) {
    learningDropdown()
  }
  if (document.querySelector(".opportunities-dropdown-box")) {
    opportunitiesDropdown()
  }
}

function opportunitiesDropdown() {
  document.querySelector(".opportunities-dropdown-hidden-box").classList.toggle("opportunities-dropdown-box");
  document.querySelector(".opportunities-menu-heading-inactive").classList.toggle("opportunities-menu-heading-active");
  document.querySelector(".drp-down-btn3").classList.toggle("drp-down-btn-flipped");
  if (document.querySelector(".learning-dropdown-box")) {
    learningDropdown()
  }
  if (document.querySelector(".challenge-dropdown-box")) {
    challengeDropdown()
  }
}

function userDropdown() {
  document.querySelector(".user-dropdown-hidden").classList.toggle('user-dropdown');
}

/*fuction to turn off dropdown when clicked anywhere on window*/

/*document.addEventListener('click', function (event) {
  var target = event.target;
  console.log(target)
  if (document.querySelector('.user-dropdown') && target!=document.querySelector('.user-login-button') && target!=document.querySelector('.userimg-box') && target!=document.querySelector('.dropdown-element')) {
    userDropdown()
  }
});*/