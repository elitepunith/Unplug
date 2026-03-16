# Unplug

A minimalist focus timer that knows when you get distracted.

## What is it?

Unplug is a straightforward productivity tool designed to encourage deep work. It strips away complex reward systems, heavy UI, and background noise in favor of a single, highly effective mechanic: accountability.

Before you start, you declare exactly what you are working on. If you leave the tab to check social media or browse the web, the app detects it, pauses your timer, and logs the interruption. It forces you to be mindful of your context switching.

## How it works

The core logic relies entirely on the vanilla JavaScript Page Visibility API.

* You enter a task intent and start the session.
* If you open a new tab, switch windows, or minimize the browser, the `visibilitychange` event is triggered.
* The app catches this state change, instantly pauses the timer, and increments your interruption counter.
* You are forced to manually click "Resume" to continue, breaking the habit loop of mindless browsing.

## Tech Stack

This project is completely vanilla. No frameworks, no build steps, and no backend.

* HTML5 (Semantic structure)
* CSS3 (Custom properties, brutalist design)
* JavaScript (ES6, DOM manipulation, Page Visibility API)

## Setup and Usage

Because there are no dependencies, getting this running locally takes zero effort.

1. Clone this repository or download the files.
2. Open `index.html` in your web browser of choice.
3. Type in your current task and click "Lock In".

## Future Roadmap

* LocalStorage integration to save total focus hours over time without requiring a database or user login.
* A "Strict Mode" toggle that completely kills the session instead of just pausing it when focus is lost.

## License

MIT