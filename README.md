                                  AI-Powered CLI Assistant
A conversational, AI-driven command-line interface that understands natural language, executes shell commands behind the scenes, and returns summarized, human-friendly responses — replacing the need to know terminal syntax.

🚀 Features
🗣️ Accepts natural language queries (e.g., “Check if Python is installed”)
🛠️ Converts input to shell commands using GPT-4 (or other LLMs)
⚙️ Executes commands silently and safely
📘 Explains what each command does (optional)
📤 Summarizes command output into plain English
🧠 Remembers context for follow-up instructions
🔐 Includes safety guardrails to prevent dangerous operations
📊 Logs all activity for optional PowerBI or analytics integration



🧪 Getting Started

# Clone the repository
git clone https://github.com/your-username/ai-cli-assistant.git
cd ai-cli-assistant

# Create virtual environment & install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
Create a .env file inside config/:

OPENAI_API_KEY=your_openai_api_key

# Run the chatbot
streamlit run app.py


💬 Example Usage
🔍 You: Show me files modified today
🤖 Bot: Found 3 files modified in the last 24 hours. Top 3:
       - report.txt
       - summary.csv
       - logs/error.log