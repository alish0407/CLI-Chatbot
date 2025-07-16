# core/output_summarizer.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from core.prompt_templates import get_prompt_template

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/.env'))
load_dotenv(dotenv_path=dotenv_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-instruct")

# Initialize Groq-compatible client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def summarize_output(command: str, output: str) -> str:
    if not output.strip():
        return "⚠️ No output to summarize."

    prompt_template = get_prompt_template("summarize")
    prompt = prompt_template.format(command=command, output=output)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Failed to summarize output (Groq): {str(e)}"
