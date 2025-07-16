import os
from dotenv import load_dotenv
import streamlit as st
from core.command_generator import generate_command
from core.command_explainer import explain_command
from core.command_executor import execute_command
from core.output_summarizer import summarize_output
from core.safety_guard import is_command_dangerous, danger_reason
from core.context_manager import ContextManager

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/.env'))
load_dotenv(dotenv_path=dotenv_path)

st.set_page_config(page_title="AI-Powered CLI Chatbot", page_icon="🤖")

# Initialize context and state
context = ContextManager()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

st.title("🤖 AI-Powered CLI Chatbot")
st.markdown(f"📁 **Current Directory:** `{st.session_state.cwd}`")

# Input form
with st.form("instruction_form"):
    instruction = st.text_input("💬 What would you like to do?", placeholder="e.g., List all files modified today")
    submitted = st.form_submit_button("Submit")

# Process on submit
if submitted and instruction:
    shell_command = generate_command(instruction)
    explanation = explain_command(shell_command)

    # Detect 'cd' command and update virtual working directory
    if shell_command.strip().lower().startswith("cd "):
        parts = shell_command.strip().split(maxsplit=1)
        if len(parts) == 2:
            new_path = os.path.abspath(os.path.join(st.session_state.cwd, parts[1]))
            if os.path.isdir(new_path):
                st.session_state.cwd = new_path
                st.success(f"📂 Changed directory to: `{new_path}`")
            else:
                st.warning(f"⚠️ Directory not found: `{new_path}`")
    else:
        # Check if command is dangerous
        is_danger = is_command_dangerous(shell_command)

        # Prompt for confirmation if dangerous
        if is_danger:
            st.warning(danger_reason(shell_command))
            confirm_checkbox = st.checkbox("☑️ I understand the risk and want to execute this command.")
            if confirm_checkbox:
                if st.button("🚨 Run Dangerous Command"):
                    confirmed = True
                else:
                    confirmed = False
            else:
                confirmed = False
        else:
            confirmed = True


        # Execute if allowed
        if confirmed:
            result = execute_command(shell_command, cwd=st.session_state.cwd)

            if result["success"]:
                summary = summarize_output(shell_command, result["output"])
                context.add(instruction, shell_command, result["output"])
            else:
                summary = ""

            # Add to history
            st.session_state.chat_history.append({
                "instruction": instruction,
                "command": shell_command,
                "explanation": explanation,
                "output": result["output"],
                "error": result["error"],
                "summary": summary
            })
        else:
            st.session_state.chat_history.append({
                "instruction": instruction,
                "command": shell_command,
                "explanation": explanation,
                "output": "",
                "error": "Execution not confirmed.",
                "summary": ""
            })

# Display interaction history
st.subheader("📜 Session History")
for entry in reversed(st.session_state.chat_history):
    st.markdown(f"#### 💬 Instruction: `{entry['instruction']}`")
    st.markdown(f"**⚙️ Command:** `{entry['command']}`")

    with st.expander("📘 Explanation"):
        st.write(entry["explanation"])

    if entry["error"]:
        st.error(entry["error"])
    else:
        st.success("✅ Command executed successfully")
        st.code(entry["output"], language="bash")

        with st.expander("🧠 Summary"):
            st.write(entry["summary"])

# Sidebar: Persistent context
with st.sidebar:
    st.subheader("🕘 Recent Context")

    if st.button("🗑️ Clear All Context"):
        context.clear()
        st.success("✅ Context cleared.")

    for entry in reversed(context.get_all()):
        st.text(f"> {entry['instruction']}")