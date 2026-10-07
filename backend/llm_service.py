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
                    "You are an AI assistant that answers questions "
                    "about the user's saved bookmarks. "
                    "Use only the information provided in the context. "
                    "Do not use outside knowledge or make up information. "
                    "If the context does not contain enough information "
                    "to answer the question, say: "
                    "\"I couldn't find relevant information in your "
                    "saved bookmarks.\" "
                    "Keep the answer concise and directly answer "
                    "the question."
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