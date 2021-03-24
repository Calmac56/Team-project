function startTimer(time, time_full, display, displayFull) 
{
    var r = document.querySelector(':root');
    var bar = 0;

    time_split_full = splitTime(time_full)
    time_split = splitTime(time)

    displayFull.textContent = formatTime(time_split_full[0], time_split_full[1]);
    display.textContent = formatTime(time_split[0], time_split[1]);

    bar = (time_full-time)/time_full*100;
    r.style.setProperty('--timer', bar.toString() + '%');

    setInterval(function () 
    {
        time_split = splitTime(time)
        display.textContent = formatTime(time_split[0], time_split[1]);

        if (time < 0) 
        {
            timer = duration;
        }

        time = time - 1;
        bar = (time_full-time)/time_full*100;
        r.style.setProperty('--timer', bar.toString() + '%');

        if (bar >= 100) 
        {
            setTimeout(function()
            {
                doPost('true');
            }, 1000);
        }
        
    }, 1000);
}

function splitTime(time) 
{
    var time_split = time, minutes, seconds;
 
    minutes = parseInt(time_split / 60, 10);
    seconds = parseInt(time_split % 60, 10);

    return [minutes, seconds];
}

function formatTime(minutes, seconds) 
{
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    return(minutes + ":" + seconds);
}