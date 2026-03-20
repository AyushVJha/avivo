# Mini-RAG Telegram Bot

A Telegram bot that answers questions from a local knowledge base using Retrieval-Augmented Generation (RAG). Built with a local embedding model and a free LLM API.


## What It Does

The bot accepts natural language questions via Telegram and responds with answers grounded in documents you provide. It does not rely on the model's general knowledge — every answer is retrieved from and constrained to your document set.

It maintains conversation history per user, caches query embeddings to avoid redundant computation, and cites the source document alongside every response.


## How It Works

When a user sends a query, the bot embeds it using a local sentence transformer model and computes cosine similarity against pre-embedded chunks of your documents. The top three matching chunks are passed as context to an LLM, which generates a concise answer. The source filename is included in every reply.

Conversation history (last three exchanges) is kept in memory per user and passed to the LLM on each call, giving the model context for follow-up questions. Query embeddings are cached so the same query is never re-embedded.


## Project Structure

    bot.py          Telegram command handlers and application entry point
    rag.py          Document loading, chunking, embedding, and retrieval
    llm.py          Prompt construction and Groq API call
    docs/           Knowledge base documents (.txt or .md files)
    requirements.txt
    .env.example


## Setup

Install dependencies:

    pip install -r requirements.txt

Create your environment file:

    cp .env.example .env

Fill in your keys:

    TELEGRAM_TOKEN=your_telegram_bot_token
    GROQ_API_KEY=your_groq_api_key

Get a Telegram token from @BotFather on Telegram. Get a free Groq API key from console.groq.com.

Run the bot:

    python bot.py


## Commands

    /start              Introduction and usage instructions
    /ask <question>     Query the knowledge base
    /summarize          Summarize the current conversation
    /help               Show available commands


## Models

    Embeddings    all-MiniLM-L6-v2 via sentence-transformers
                  Runs entirely locally. No API calls, no cost.
                  Chosen for its balance of speed and semantic quality at a small model size.

    LLM           llama-3.1-8b-instant via Groq API
                  Free tier, no credit card required.
                  Chosen because RAG does not require a large model — the model only needs
                  to read a short context and summarize it. 8B parameters is sufficient.


## Adding Your Own Documents

Drop any .txt or .md file into the docs/ folder and restart the bot. No other changes needed.