let flickBtn = document.getElementById('flick-btn');
let turnEl = document.getElementById('turn');
let formEl = document.getElementById('hidden-form');
let input = document.getElementById('hidden-input');

flickBtn.addEventListener('click', flick);

async function flick() {
  let options = ['left', 'hit', 'right'];
  let move = options[Math.floor(Math.random() * 3)];
  turnEl.className = 'turn ' + move;
  turnEl.src = input.value = move === 'hit' ? 'hit' : 'miss';

  setTimeout(() => {
    formEl.submit();
  }, 2000);
}
