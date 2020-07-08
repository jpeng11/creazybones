let flickBtn = document.getElementById('flick-btn');
let turnEl = document.getElementById('turn');
let formEl = document.getElementById('hidden-form');
let input = document.getElementById('hidden-input');

flickBtn.addEventListener('click', flick);

async function flick() {
  let options = ['left', 'hit', 'right'];
  let move = options[Math.floor(Math.random() * 3)];
  turnEl.className = 'turn ' + move;
  setTimeout(() => {
    turnEl.src =
      move === 'hit'
        ? 'https://www.pngfind.com/pngs/m/538-5380909_pow-png-comic-clipart-transparent-png.png'
        : 'http://www.atthakorn.com/wp-content/uploads/2015/12/whoosh1.jpg';
  }, 1000);
  input.value = move === 'hit' ? 'hit' : 'miss';

  setTimeout(() => {
    formEl.submit();
  }, 2000);
}
