import os
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from github import Github

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repo-name

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Smith is active and listening. Use /pull <filename.py> or send a .py file to push.")

async def pull_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /pull <filename.py>")
        return

    file_name = context.args[0]
    try:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{file_name}"
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
            await update.message.reply_document(document=InputFile(file_name))
            os.remove(file_name)
        else:
            await update.message.reply_text(f"Error fetching file: {response.status_code} - Not Found")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document and document.file_name.endswith(".py"):
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        content_str = file_content.decode("utf-8")

        try:
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(GITHUB_REPO)
            file_path = document.file_name

            try:
                contents = repo.get_contents(file_path)
                repo.update_file(contents.path, f"Updated {file_path}", content_str, contents.sha)
                await update.message.reply_text(f"{file_path} updated successfully on GitHub.")
            except:
                repo.create_file(file_path, f"Created {file_path}", content_str)
                await update.message.reply_text(f"{file_path} created and pushed to GitHub.")

        except Exception as e:
            await update.message.reply_text(f"GitHub Error: {str(e)}")
    else:
        await update.message.reply_text("Please send a valid .py file.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pull", pull_file))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()


    app.run_polling()

if __name__ == "__main__":
    main()
