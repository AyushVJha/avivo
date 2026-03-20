import os
from groq import Groq


def answer(query, context_chunks, history=None):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    context = "\n\n".join(
        f"[{c['source']}]\n{c['text']}" for c in context_chunks
    )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer using only the provided context. Be concise."
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}"
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()


def summarize(conversation):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following conversation concisely."
            },
            {
                "role": "user",
                "content": conversation
            }
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()