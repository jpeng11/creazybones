console.log("Connected");
// DOM Elements
formYesBtns = document.querySelectorAll("form .Yes");
formNoBtns = document.querySelectorAll("form .No");
popupEl = document.querySelector('#popup')
popupElText = document.querySelector('#popup p')
popupYesBtns = document.querySelector("#popup .Yes");
popupNoBtns = document.querySelector("#popup .No");

// State
let form = null;
let input = null;

// Events
formYesBtns.forEach((yesBtn) => {
  yesBtn.onclick = function (event) {
    event.preventDefault();
    popupElText.innerText = "Are you sure you want to make this trade?"
    popupEl.style.display = "flex"
    form = event.target.parentElement;
    input = document.getElementById("accept_trade_" + form.id)
    input.value = "Yes"
  }
})

formNoBtns.forEach((noBtn) => {
  noBtn.onclick = function (event) {
    event.preventDefault();
    popupElText.innerText = "Are you sure you want to reject this trade?"
    popupEl.style.display = "flex"
    form = event.target.parentElement;
    input = document.getElementById("accept_trade_" + form.id)
    input.value = "No"
  }
})

popupYesBtns.onclick = function () {
  form.submit();
}

popupNoBtns.onclick = function () {
  popupEl.style.display = "none"
  form = null;
  input.value = "";
  input = null;
}