import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import rag
import llm

load_dotenv()
rag.load_docs()

user_history = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello. Use /ask <your question> to query the knowledge base.\n"
        "Use /help to see all commands."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ask <query>       Ask a question from the knowledge base\n"
        "/summarize         Summarize your conversation so far\n"
        "/help              Show this message"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()

    if not query:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    user_id = update.effective_user.id
    history = user_history.get(user_id, [])

    top_chunks = rag.retrieve(query)
    response = llm.answer(query, top_chunks, history)

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})
    user_history[user_id] = history[-6:]

    sources = ", ".join(sorted(set(c["source"] for c in top_chunks)))
    await update.message.reply_text(f"{response}\n\nSources: {sources}")


async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = user_history.get(user_id, [])

    if not history:
        await update.message.reply_text("No conversation history to summarize.")
        return

    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in history
    )
    summary = llm.summarize(conversation)
    await update.message.reply_text(summary)


if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN is not set in .env")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("summarize", summarize))

    print("Bot is running...")
    app.run_polling()