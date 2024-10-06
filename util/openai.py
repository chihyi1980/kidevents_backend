from config import Config
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY, organization=Config.OPENAI_ORG)


def chat(msg):
    try:
        model = 'gpt-4o-mini'
        messages=[
            {
                "role": "user",
                "content": msg
            }
        ]

        response = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = 0
        )

        # 返回模型回應中的文字
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


