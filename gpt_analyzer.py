import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def analyze_text(extracted_text):
    prompt = f"""
    You are an AI assistant for the game XCOM 2. Based on the following game screen text, provide strategic advice:
    {extracted_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message['content']