import os
from dotenv import load_dotenv
from openai import OpenAI
from core.prompt_templates import get_prompt_template

# Load .env variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/.env'))
load_dotenv(dotenv_path=dotenv_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mistral-saba-24b")

# Initialize client with Groq base URL
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_command(instruction: str) -> str:
    prompt_template = get_prompt_template("generate")
    prompt = prompt_template.format(instruction=instruction)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Failed to generate command (Groq): {str(e)}"
