import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL")

def generate_answer(question, context):
    response = client.responses.create(
        model = MODEL,
        input = [
            {
                "role": "system",
                "content": (
                    "You answer questions using only the provided context. "
                    "If the context does not contain the answer, "
                    "say that you don't know."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                )
            }
        ]
    )

    return response.output_text