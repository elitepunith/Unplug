// Grab our DOM elements
const timerDisplay = document.getElementById('timer-display');
const btnUnplug = document.getElementById('btn-unplug');
const statusText = document.getElementById('status-text');
const wrapper = document.querySelector('.terminal-container');
const warningText = document.getElementById('glitch-warning');

// State variables
let timerInterval = null;
let secondsActive = 0;
let isRunning = false;

// Format the time so it looks like 00:00 instead of just a raw number
function updateDisplay() {
    const m = Math.floor(secondsActive / 60).toString().padStart(2, '0');
    const s = (secondsActive % 60).toString().padStart(2, '0');
    timerDisplay.innerText = `${m}:${s}`;
}

// Kick off the timer
function startTerminal() {
    if (isRunning) return; 
    
    isRunning = true;
    statusText.innerText = "LINK ESTABLISHED. DO NOT LOOK AWAY.";
    btnUnplug.classList.add('hidden'); // hide button while running
    warningText.classList.add('hidden');
    
    // Reset any previous glitch effects just in case
    wrapper.classList.remove('shatter');
    
    timerInterval = setInterval(() => {
        secondsActive++;
        updateDisplay();
    }, 1000);
}

// Nuke it. They left the tab.
function triggerGlitch() {
    clearInterval(timerInterval);
    isRunning = false;
    secondsActive = 0; // zero out their progress lol
    updateDisplay();
    
    // update the UI to look broken
    statusText.innerText = "SYSTEM FAILURE.";
    wrapper.classList.add('shatter');
    warningText.classList.remove('hidden');
    
    // bring the button back so they can try again
    setTimeout(() => {
        btnUnplug.innerText = "REBOOT SYSTEM";
        btnUnplug.classList.remove('hidden');
    }, 1000);
}

// --- EVENT LISTENERS ---

// Button click
btnUnplug.addEventListener('click', () => {
    startTerminal();
});

// The core mechanic: checking if they switch tabs
// Using the visibility API because it's super reliable for this
document.addEventListener('visibilitychange', () => {
    // If the timer is actually running and the tab becomes hidden...
    if (isRunning && document.visibilityState === 'hidden') {
        console.log("User lost focus, triggering penalty.");
        triggerGlitch();
    }
});