// main.js
// handles all the timer + tab detection stuff
// wrote this in a few sittings so it might be a little inconsistent

var taskInput    = document.getElementById('task-input');
var startBtn     = document.getElementById('start-btn');
var resumeBtn    = document.getElementById('resume-btn');
var endBtn       = document.getElementById('end-btn');
var timerEl      = document.getElementById('timer-display');
var taskLabel    = document.getElementById('task-label');
var countEl      = document.getElementById('interruption-count');
var statusMsg    = document.getElementById('status-message');
var setupDiv     = document.getElementById('setup-section');
var focusDiv     = document.getElementById('focus-section');

// state
let secs = 0;
let lapses = 0;      // "interruptions" felt too judgmental in variable form lol
let ticker = null;
let running = false;

function pad(n) {
    return String(n).padStart(2, '0');
}

function showTime() {
    let m = Math.floor(secs / 60);
    let s = secs % 60;
    timerEl.textContent = pad(m) + ':' + pad(s);
}

function startTicking() {
    // make sure we don't stack intervals - got burned by this before
    if (ticker) clearInterval(ticker);
    ticker = setInterval(function() {
        secs++;
        showTime();
    }, 1000);
    running = true;
}

function beginSession() {
    var task = taskInput.value.trim();
    if (!task) {
        // could do a shake animation here but this works for now
        taskInput.focus();
        return;
    }

    taskLabel.textContent = task;
    setupDiv.classList.add('hidden');
    focusDiv.classList.remove('hidden');

    startTicking();
}

function pauseOnTabLeave() {
    clearInterval(ticker);
    running = false;
    statusMsg.classList.remove('hidden');
    resumeBtn.classList.remove('hidden');
    lapses++;
    countEl.textContent = lapses;
}

function resumeSession() {
    statusMsg.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    startTicking();
}

function endSession() {
    clearInterval(ticker);
    ticker = null;

    // reset everything back to zero
    secs = 0;
    lapses = 0;
    running = false;

    timerEl.textContent = '00:00';
    countEl.textContent = '0';
    taskInput.value = '';
    taskLabel.textContent = '...';

    statusMsg.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    focusDiv.classList.add('hidden');
    setupDiv.classList.remove('hidden');

    // slight delay so the reset doesn't feel instant
    setTimeout(() => taskInput.focus(), 50);
}

startBtn.addEventListener('click', beginSession);
endBtn.addEventListener('click', endSession);
resumeBtn.addEventListener('click', resumeSession);

taskInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') beginSession();
});

// catches tab switches / window minimise
document.addEventListener('visibilitychange', function() {
    if (running && document.visibilityState === 'hidden') {
        pauseOnTabLeave();
    }
});

// TODO: maybe save best session to localStorage at some point
