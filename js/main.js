// main.js
// this grew a lot from what it started as

var taskInput        = document.getElementById('task-input');
var startBtn         = document.getElementById('start-btn');
var resumeBtn        = document.getElementById('resume-btn');
var endBtn           = document.getElementById('end-btn');
var againBtn         = document.getElementById('again-btn');
var newTaskBtn       = document.getElementById('new-task-btn');
var timerEl          = document.getElementById('timer-display');
var taskLabel        = document.getElementById('task-label');
var modeLabelEl      = document.getElementById('mode-label');
var countEl          = document.getElementById('interruption-count');
var timeLostEl       = document.getElementById('time-lost');
var statusMsg        = document.getElementById('status-message');
var setupDiv         = document.getElementById('setup-section');
var focusDiv         = document.getElementById('focus-section');
var summaryDiv       = document.getElementById('summary-section');
var progressWrap     = document.getElementById('progress-wrap');
var progressBar      = document.getElementById('progress-bar');
var historySection   = document.getElementById('history-section');
var historyList      = document.getElementById('history-list');
var summaryTaskName  = document.getElementById('summary-task-name');
var summaryTimeEl    = document.getElementById('summary-time');
var summaryInterruptions = document.getElementById('summary-interruptions');
var summaryLost      = document.getElementById('summary-lost');
var summaryScore     = document.getElementById('summary-score');
var summaryVerdict   = document.getElementById('summary-verdict');
var modeBtns         = document.querySelectorAll('.mode-btn');

let secs         = 0;
let lapses       = 0;        // "interruptions" felt too judgmental in variable form lol
let timeLostSecs = 0;
let ticker       = null;
let running      = false;
let selectedMins = 0;
let tabLeftAt    = null;     // timestamp of when they bailed
let currentTask  = '';


// ---- mode picker ----

modeBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        modeBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedMins = parseInt(this.dataset.mins);
    });
});


// ---- formatting helpers ----

function pad(n) {
    return String(n).padStart(2, '0');
}

function fmt(totalSecs) {
    let m = Math.floor(totalSecs / 60);
    let s = totalSecs % 60;
    return pad(m) + ':' + pad(s);
}

// shows seconds under a minute, then "1m 20s" style above that
function fmtLost(s) {
    if (s === 0) return '0s';
    if (s < 60) return s + 's';
    let m = Math.floor(s / 60);
    let rem = s % 60;
    return rem > 0 ? m + 'm ' + rem + 's' : m + 'm';
}

// 0–100, penalises heavily for early bails and time lost
function calcScore(focusSecs, lapses, lostSecs) {
    if (focusSecs < 10) return '—';
    let total = focusSecs + lostSecs;
    if (total === 0) return '100';
    let base = focusSecs / total * 100;
    let penalty = lapses * 4;
    return Math.max(0, Math.round(base - penalty));
}


// ---- timer ----

function showTime() {
    timerEl.textContent = fmt(secs);

    if (selectedMins > 0) {
        let target = selectedMins * 60;
        progressBar.style.width = Math.min((secs / target) * 100, 100) + '%';
        if (secs >= target) {
            handleTimerDone();
        }
    }
}

function startTicking() {
    if (ticker) clearInterval(ticker);   // burned by double intervals before, never again
    ticker = setInterval(function() {
        secs++;
        showTime();
    }, 1000);
    running = true;
}


// ---- session lifecycle ----

function beginSession() {
    var task = taskInput.value.trim();
    if (!task) {
        taskInput.focus();
        taskInput.classList.add('shake');
        setTimeout(() => taskInput.classList.remove('shake'), 400);
        return;
    }

    currentTask  = task;
    secs         = 0;
    lapses       = 0;
    timeLostSecs = 0;
    tabLeftAt    = null;

    taskLabel.textContent   = task;
    countEl.textContent     = '0';
    timeLostEl.textContent  = '0s';
    timerEl.classList.remove('done');
    showTime();

    if (selectedMins > 0) {
        modeLabelEl.textContent = selectedMins + ' min session';
        progressWrap.classList.remove('hidden');
        progressBar.style.width = '0%';
    } else {
        modeLabelEl.textContent = 'open session';
        progressWrap.classList.add('hidden');
    }

    statusMsg.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    setupDiv.classList.add('hidden');
    focusDiv.classList.remove('hidden');

    startTicking();
}

function pauseOnTabLeave() {
    clearInterval(ticker);
    running   = false;
    tabLeftAt = Date.now();

    lapses++;
    countEl.textContent = lapses;
    statusMsg.classList.remove('hidden');
    resumeBtn.classList.remove('hidden');
}

function resumeSession() {
    if (tabLeftAt !== null) {
        let awaySecs = Math.round((Date.now() - tabLeftAt) / 1000);
        timeLostSecs += awaySecs;
        timeLostEl.textContent = fmtLost(timeLostSecs);
        tabLeftAt = null;
    }
    statusMsg.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    startTicking();
}

function handleTimerDone() {
    clearInterval(ticker);
    ticker  = null;
    running = false;
    timerEl.classList.add('done');
    // small pause so they can see it hit the target before summary kicks in
    setTimeout(showSummary, 900);
}

function endSession() {
    clearInterval(ticker);
    ticker  = null;
    running = false;
    showSummary();
}


// ---- summary ----

function getVerdict(lapses, lostSecs, focusSecs) {
    if (focusSecs < 30) return 'barely started. that counts as a warmup.';
    if (lapses === 0) return 'clean. no slips. seriously good.';
    if (lapses === 1 && lostSecs < 30) return 'one slip, caught it fast. solid.';
    if (lapses <= 2 && lostSecs < 90) return 'distracted but you came back. that\'s the move.';
    if (lapses <= 4) return 'rough around the edges. still showed up.';
    return 'scattered one. happens. tomorrow\'s another shot.';
}

function showSummary() {
    // if they left and never came back, count that time too
    if (tabLeftAt !== null) {
        timeLostSecs += Math.round((Date.now() - tabLeftAt) / 1000);
        tabLeftAt = null;
    }

    let score = calcScore(secs, lapses, timeLostSecs);

    summaryTaskName.textContent         = currentTask;
    summaryTimeEl.textContent           = fmt(secs);
    summaryInterruptions.textContent    = lapses;
    summaryLost.textContent             = fmtLost(timeLostSecs);
    summaryScore.textContent            = typeof score === 'number' ? score : score;
    summaryVerdict.textContent          = getVerdict(lapses, timeLostSecs, secs);

    focusDiv.classList.add('hidden');
    summaryDiv.classList.remove('hidden');

    saveSession(currentTask, secs, lapses, timeLostSecs);
}


// ---- reset helpers ----

function resetToSetup(keepTask) {
    clearInterval(ticker);
    ticker       = null;
    secs         = 0;
    lapses       = 0;
    timeLostSecs = 0;
    running      = false;
    tabLeftAt    = null;

    timerEl.textContent     = '00:00';
    timerEl.classList.remove('done');
    countEl.textContent     = '0';
    timeLostEl.textContent  = '0s';
    taskLabel.textContent   = '...';

    if (!keepTask) taskInput.value = '';

    statusMsg.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    summaryDiv.classList.add('hidden');
    focusDiv.classList.add('hidden');
    setupDiv.classList.remove('hidden');

    loadHistory();
    setTimeout(() => taskInput.focus(), 50);
}


// ---- localStorage ----

function saveSession(task, secs, lapses, lost) {
    let history = loadRaw();
    history.unshift({ task, secs, lapses, lost, date: Date.now() });
    history = history.slice(0, 8);
    try {
        localStorage.setItem('unplug_v2', JSON.stringify(history));
    } catch(e) {
        // storage full or blocked, not worth crashing over
    }
}

function loadRaw() {
    try {
        return JSON.parse(localStorage.getItem('unplug_v2') || '[]');
    } catch(e) {
        return [];
    }
}

function loadHistory() {
    let history = loadRaw();
    if (history.length === 0) {
        historySection.classList.add('hidden');
        return;
    }

    historySection.classList.remove('hidden');
    historyList.innerHTML = '';

    history.forEach(entry => {
        let li   = document.createElement('li');
        let date = new Date(entry.date);
        let dateStr = date.toLocaleDateString('en', { month: 'short', day: 'numeric' });

        let slipWord = entry.lapses === 1 ? 'slip' : 'slips';
        let meta = dateStr + ' · ' + fmt(entry.secs) + ' · ' + entry.lapses + ' ' + slipWord;

        let task = document.createElement('span');
        task.className   = 'h-task';
        task.textContent = entry.task;

        let info = document.createElement('span');
        info.className   = 'h-meta';
        info.textContent = meta;

        li.appendChild(task);
        li.appendChild(info);
        historyList.appendChild(li);
    });
}


// ---- events ----

startBtn.addEventListener('click', beginSession);
endBtn.addEventListener('click', endSession);
resumeBtn.addEventListener('click', resumeSession);
againBtn.addEventListener('click', () => resetToSetup(true));    // same task, go again
newTaskBtn.addEventListener('click', () => resetToSetup(false)); // start fresh

taskInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') beginSession();
});

document.addEventListener('visibilitychange', function() {
    if (running && document.visibilityState === 'hidden') {
        pauseOnTabLeave();
    }
});


// ---- init ----

loadHistory();