function startCountdown(secondsRemaining) {

    const countdownElement = document.getElementById('countdown');
    //console.log("in start countdown");
    const interval = setInterval(function () {
        //console.log("in interval func");
        if (secondsRemaining <= 0) {
            clearInterval(interval);
            countdownElement.textContent = 'Countdown finished!';
        } else {
            countdownElement.textContent = `${secondsRemaining} second remain`;
            secondsRemaining--;

            localStorage.setItem('countdown', secondsRemaining);
        }
    }, 1000);
}

const savedCountdown = localStorage.getItem('countdown');

if (savedCountdown) {
    //console.log("saved countdown");
    const secondsRemaining = parseInt(savedCountdown);
    startCountdown(secondsRemaining);
} else {
    //console.log(" not saved countdown");
    const initialSeconds = 3600; // 1 ���
    startCountdown(initialSeconds);
}