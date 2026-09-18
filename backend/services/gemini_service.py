from google import genai
import os
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, chunks):
    context = "\n\n".join(chunks)

    prompt = f"""
Answer the user's question using ONLY the provided document context.

If the answer is not present in the context, say:
"I couldn't find this information in the uploaded document."

Do not use outside knowledge.

Document context:
{context}

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text