import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_llm_response(context,question):
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer only from the given context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    )
    return response.choices[0].message.content