# 🤖AutoTask - Agentic Android Automation 

**Droidrun DevSprint 2026 | GDG on Campus IIT Patna**

AutoTask is an agentic Android automation system that allows users to control and automate Android applications using natural language. Built using Droidrun's Agent Framework, the system plans tasks intelligently and executes them on real Android devices using UI automation.

## 🔥Why this project stands out 
Most Android automation tools are rule-based and fragile. This project goes beyond scripts.
This agent understands intent. 

**Give it a task line:** 
"Open Settings and turn on WiFi"

It autonomously: <br>
1. Understands the goal
2. Breaks it into steps
3. Executes actions on Android(or simulates them intelligently)

This is true Agentic Automation, not macros.

## 🧠What problem does it solve? 
Mobile workflows are repetitive, UI-heavy, and inaccessible to non-technical users. Existing automation requires:
• Manual scripting 
• App-specific rules 
• Frequent breakage on UI changes
This project removes that friction by enabling natural language control over Android apps.

## 🏗️Architecture
User Input (Natural Language) <br>
    ↓ <br>
LLM-based Planner<br>
    ↓ <br>
Execution Plan (Steps) <br>
    ↓ <br>
Android Action Engine (uiautomator2) <br>
    ↓ <br>
Task Completion + Memory <br>

## Key Capabilities 
• Task Planning - Converts intent into step-by-step plans 
• Agentic Execution - Executes actions autonomously 
• Self-healing - Can re-plan on failure 
• Mock Mode - Demo-ready without device or paid APIs 
• Real Device Ready - Work on USB-connected Android

## Demo (Hackathon Mode) <br>
To ensure smooth judging, the system supports MOCK MODE: <br>
• No Android device required <br>
• No paid API calls <br>
• Fully simulated execution with logs  <br>
**Example demo task**: 
Open settings and turn on WiFi <br>
**Output**:
• Generated plan 
• Executed steps
• Successful task completion 
This guarantees reliable demo videos under hackathon constraints.

## 📂Project Structure
autotask-agentic-android/ <br>
├── autotask_agent/       <br>
│   ├── __init__.py       <br>
│   ├── agent.py          # Main agent orchestrator <br>
│   ├── planner.py        # AI-powered task planning <br>
│   ├── actions.py        # Low-level Android actions <br>
│   └── memory.py         # Persistent learning system <br>
├── prompts/              # AI prompts and templates <br>
├── demos/                # Demo scripts and videos  <br>
├── run_agent.py          # CLI runner <br>
├── README.md                 <br>
└── requirements.txt          <br>

## 🛠️Tech Stack
- **Python 3.12** <br>
- **Droidrun Agent Framework** <br>
- **uiautomator2 (Android control)** <br>
- **LLM-based Planning** <br>
- **Loguru(clean execution logs)** <br>
- **dotenv (secure config)** <br>

## 🎯Use Cases 
• Accessibility automation for elderly users 
• Personal mobile assistants
• QA testing & app navigation
• Productivity workflows 
• No-code Android automation

## 📝License
MIT License

## 👤Author
Solo Participant - Droidrun DevSprint 2026
• Alok - Built under extreme time constraints with a focus on clarity, agentic design, and real-world impact.

## 📧Contact Details 
**G-mail**:alok844937@gmail.com<br>
**Demo Video**: https://youtu.be/gpYgtLIwDRI?si=tTeoxLv7tPXgH9lC <br>
**GitHub**: https://github.com/alok844937-design
