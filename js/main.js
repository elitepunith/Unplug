// Grab DOM elements
const setupSection = document.getElementById('setup-section');
const focusSection = document.getElementById('focus-section');
const taskInput = document.getElementById('task-input');
const startBtn = document.getElementById('start-btn');
const resumeBtn = document.getElementById('resume-btn');
const endBtn = document.getElementById('end-btn');

const timerDisplay = document.getElementById('timer-display');
const taskDisplay = document.querySelector('#current-task span');
const interruptionDisplay = document.getElementById('interruption-count');
const statusMessage = document.getElementById('status-message');

// App state
let timerInterval;
let seconds = 0;
let interruptions = 0;
let isRunning = false;

// format time into mm:ss
function formatTime(totalSeconds) {
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const s = (totalSeconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

// update the visual timer
function tick() {
    seconds++;
    timerDisplay.innerText = formatTime(seconds);
}

// Start the focus session
function startSession() {
    // don't start if they didn't type anything
    if (taskInput.value.trim() === "") {
        alert("Enter a task first.");
        return;
    }

    // swap UI
    setupSection.classList.add('hidden');
    focusSection.classList.remove('hidden');
    taskDisplay.innerText = taskInput.value;
    
    // kick off the timer
    isRunning = true;
    timerInterval = setInterval(tick, 1000);
}

// Pause session (used when they tab out)
function pauseSession() {
    clearInterval(timerInterval);
    isRunning = false;
    
    // show the resume button and warning
    statusMessage.classList.remove('hidden');
    resumeBtn.classList.remove('hidden');
}

// Resume after being distracted
function resumeSession() {
    statusMessage.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    
    isRunning = true;
    timerInterval = setInterval(tick, 1000);
}

// End the whole thing and reset
function endSession() {
    clearInterval(timerInterval);
    
    // reset state
    seconds = 0;
    interruptions = 0;
    isRunning = false;
    taskInput.value = "";
    timerDisplay.innerText = "00:00";
    interruptionDisplay.innerText = "0";
    
    // reset UI visibility
    statusMessage.classList.add('hidden');
    resumeBtn.classList.add('hidden');
    focusSection.classList.add('hidden');
    setupSection.classList.remove('hidden');
}


// --- Events ---

startBtn.addEventListener('click', startSession);
resumeBtn.addEventListener('click', resumeSession);
endBtn.addEventListener('click', endSession);

// allow hitting Enter to start
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startSession();
});

// The snitch: check if they leave the tab
document.addEventListener('visibilitychange', () => {
    // only punish them if the timer is actively running
    if (isRunning && document.visibilityState === 'hidden') {
        interruptions++;
        interruptionDisplay.innerText = interruptions;
        pauseSession();
    }
});