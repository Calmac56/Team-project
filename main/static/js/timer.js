function startTimer(duration, display, displayFull) {
    var r = document.querySelector(':root');
    var timer = duration, minutes, seconds;
    var durationtot = duration;
    var bar = 0;

    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    displayFull.textContent = minutes + ":" + seconds;
    display.textContent = minutes + ":" + seconds;

    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }

        durationtot = durationtot - 1;
        bar = (duration-durationtot)/duration*100;
        r.style.setProperty('--timer', bar.toString() + '%');

        if (bar == 100) {
            setTimeout(function(){
                doPost('true');
            }, 1000);
        }
        
    }, 1000);
}