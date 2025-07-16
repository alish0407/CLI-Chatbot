from core.os_utils import get_os_type 

WINDOWS_TEMPLATES = {
    "generate": """
You are a helpful assistant that converts natural language instructions into Windows Command Prompt (CMD) commands.

- Only generate commands compatible with CMD or PowerShell on Windows.
- Do not include any explanation or markdown formatting.
- Output a single line command only.

Examples:
- "list all files" → `dir`
- "delete all directories" → for /d %G in (*) do rd /s /q "%G"

Instruction: {instruction}
CMD:
""",
    "explain": """
You are an expert in Windows command-line utilities.

Your job is to explain the following Windows CMD command in simple, beginner-friendly language.


Command: {command}

Explain what this command does step-by-step:
""",
    "summarize": """
You are a helpful assistant.

Here is the output from a Windows command:
---
Command: {command}
Output:
{output}
---

Summarize what this output means in simple terms. If it's an error, describe the issue and possible fix.
"""
}

LINUX_TEMPLATES = {
    "generate": """
You are an intelligent Linux terminal assistant.

Convert the following natural language instruction into a safe and efficient Linux shell command.
Only output the shell command. Do NOT include any explanation or formatting.

Instruction:
{instruction}

Shell Command:
""",
    "explain": """
You are a Linux command explainer.

Explain the following shell command in plain, beginner-friendly English.
Break down each part briefly and clearly. Avoid technical jargon unless necessary.

Command:
{command}

Explanation:
""",
    "summarize": """
You are a helpful terminal assistant.

The following shell command was executed:
{command}

Here is its raw terminal output:
{output}

Now, write a clear and concise summary of the result in plain English.
Focus on key insights or what the command accomplished.

Summary:
"""
}

MAC_TEMPLATES = LINUX_TEMPLATES  # macOS uses Unix-like shell

def get_prompt_template(task: str) -> str:
    os_type = get_os_type()
    
    if os_type == "windows":
        return WINDOWS_TEMPLATES[task]
    elif os_type in ("linux", "mac"):
        return LINUX_TEMPLATES[task]
    else:
        raise ValueError("Unsupported or unknown OS")

