from google import genai
from core.monitor import collect_system_metrics
import time
from config.api_keys import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def get_ai_response(user_query):

    metrics = collect_system_metrics()

    prompt = f"""
You are a smart AI system assistant.

System Data:
CPU: {metrics['cpu']}%
RAM: {metrics['ram']}%
Disk: {metrics['disk']}%
Battery: {metrics['battery']}%

User Question:
{user_query}

Give short, clear, practical answer.
"""

    # 🔁 Retry logic
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    # 🔄 Fallback model
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

    except Exception:
        return "⚠️ AI assistant is busy. Please try again in a moment."