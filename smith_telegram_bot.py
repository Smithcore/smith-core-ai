import os
import openai
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Smith is active and listening.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = ' '.join(context.args)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Smith, a highly capable execution AI."},
                {"role": "user", "content": user_input}
            ]
        )
        await update.message.reply_text(response['choices'][0]['message']['content'])
    except Exception as e:
        await update.message.reply_text(f"[Error: {str(e)}]")

async def push(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("Attach a file with the /push command.")
        return

    file = await update.message.document.get_file()
    file_path = f"/tmp/{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    with open(file_path, "r") as f:
        content = f.read()

    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{update.message.document.file_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    get_resp = requests.get(api_url, headers=headers)
    sha = get_resp.json().get("sha")

    data = {
        "message": "Smith auto-push via Telegram",
        "content": content.encode("utf-8").decode("utf-8"),
        "branch": GITHUB_BRANCH
    }

    if sha:
        data["sha"] = sha

    response = requests.put(api_url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        await update.message.reply_text("Push to GitHub successful.")
    else:
        await update.message.reply_text(f"GitHub push failed: {response.json()}")

async def pull(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /pull filename.py")
        return

    filename = context.args[0]
    api_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{filename}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        with open(f"/tmp/{filename}", "w") as f:
            f.write(response.text)

        await update.message.reply_document(document=open(f"/tmp/{filename}", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error fetching file: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("push", push))
    app.add_handler(CommandHandler("pull", pull))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask))

    app.run_polling()

if __name__ == "__main__":
    main()
