let secret = Math.floor(Math.random() * 100) + 1;

function checkGuess() {
  const guessInput = document.getElementById('guess');
  const result = document.getElementById('result');
  const guess = parseInt(guessInput.value, 10);

  if (isNaN(guess)) {
    result.textContent = '숫자를 입력하세요.';
    return;
  }

  if (guess < secret) {
    result.textContent = '너무 작아요!';
  } else if (guess > secret) {
    result.textContent = '너무 커요!';
  } else {
    result.textContent = '정답입니다! 새로운 숫자를 생각했어요.';
    secret = Math.floor(Math.random() * 100) + 1;
  }

  guessInput.value = '';
}
