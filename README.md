# 🤖AutoTask - Agentic Android Automation 

**Droidrun DevSprint 2026 | GDG on Campus IIT Patna**

AutoTask is an agentic Android automation system that allows users to control and automate Android applications using natural language. Built using Droidrun's Agent Framework, the system plans tasks intelligently and executes them on real Android devices using UI automation.

## 🚀Problem Statement 
Performing repetitivew or multi-step tasks on mobile devices is time-consuming and error-prone. Existing automation tools require scripting or rigid rule-based flows, making them inaccessible to non-technical users.

## 💡Solution 
AutoTask enables **natural language driven Android automation**. Users describe what they want to do, and an AI-powered agent: 
1. Understands the task 
2. Breaks it into actionable steps 
3. Executes those steps autonomously on Android apps 

## 🌟Key Features
### 1. Natural Language Task Execution Users can describe tasks in plain English:
"Open WhatsApp and send 'Hello' to Alex" "Open Settings and enable Dark Mode"

### 2. Agentic Task Planning 
AN LLM-based planner converts user intent into structured step-by-step plans suitable for Android execution.

### 3. Android UI Automation 
Uses *uiautomator2 + ADB** to:
- Launch apps
- Click buttons 
- Enter Text 
- Navigate screens 

### 4. Error Handling & Recovery 
Basic retry and fallback strategies help the agent continue execution when UI elemnets are not immediately found. 

### 5. Multi-App Workflows 
Supports workfl;ows that span across multiple Android applications in a single command.

## 🏗️Architecture
User Input (Natural Language) <br>
    ↓
TaskPlanner (Claude AI) <br>
    ↓
Execution Plan (Steps) <br>
    ↓
AndroidActions (Executor) <br>
    ↓
Device UI Interaction (ADB + UIAutomator)

## 📂Project Structure
autotask-agentic-android/
├── autotask_agent/
│   ├── __init__.py
│   ├── agent.py          # Main agent orchestrator
│   ├── planner.py        # AI-powered task planning
│   ├── actions.py        # Low-level Android actions
│   └── memory.py         # Persistent learning system
├── prompts/              # AI prompts and templates
├── demos/                # Demo scripts and videos
├── run_agent.py          # CLI runner
├── README.md
└── requirements.txt

## 🛠️Tech Stack
- **Python 3.10**
- **Droidrun Agent Framework**
- **uiautomator2**
- **ADB (pure-python-adb)**
- **Anthropic / OpenAI APIs**
- **SQLite (via SQLAlchemy)**

## 💡Example Use Cases
agent.execute_task("Open WhatsApp and send 'Metting at 3 PM' to John")
agent.execute_task("Open Settings and turn on Dark Mode")
agent.execute_task("Open Gmail and check unread emails")

## 🧠Why Agentic? 
Unlike rule-based automation: 
• The agent plans dynamically 
• Adjusts execution based on app state 
• Can recover from minor UI changes

## 🔒Privacy & Safety
• Device interaction happens locally 
• Only task planning uses cloud-based LLM APIs 
• No user data is stored permanently unless explicitly required 

## 🏆Hackathon Value
Innovation
• Agent-based Android automation 
• Natural language interface for mobile workflows 

Pratical Impact 
• Reduces reptitive mobile tasks 
• Accessible to non-technicaal users

Demo Strength 
• Live execution on real Android device 
• No pre-recorded flows

## 🛠️Setup Instructions
Prerequisites 
• Android device or emulator 
• USB Debugging enabled 
• Python 3.10+

Installation 
pip install -r requirements.txt

Verify Device Connection 
adb Devices 

Run Agent 
python run_agent.py

## 📝License
MIT License

## 👤Team
Solo Participant 
• Alok - Agent Design, Android Automation, Planning & Execution

## 🙏Acknowledgments
• Anthropic Claude for AI capabilities
• uiautomator2 for Android automation
• Google for the amazing hackathon opportunity

## 📧Contact Details 
**G-mail**:alok844937@gmail.com<br>
**Demo Video**: https://youtu.be/gpYgtLIwDRI?si=tTeoxLv7tPXgH9lC <br>
**GitHub**: https://github.com/alok844937-design
