import os
import telebot
from github import Github

# Load environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

bot = telebot.TeleBot(BOT_TOKEN)
pending_push_file = {}

def push_to_github(filename):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        try:
            existing_file = repo.get_contents(filename)
            repo.update_file(existing_file.path, f"Updated {filename}", content, existing_file.sha)
        except:
            repo.create_file(filename, f"Added {filename}", content)

        return True
    except Exception as e:
        print(f"GitHub Push Error: {e}")
        return False

@bot.message_handler(commands=['push'])
def handle_push_command(message):
    global pending_push_file
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /push filename.py")
            return
        filename = parts[1]
        pending_push_file[message.chat.id] = filename
        bot.reply_to(message, f"Upload the file `{filename}` now to push it to GitHub.")
    except Exception as e:
        bot.reply_to(message, f"Push command error: {str(e)}")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global pending_push_file
    try:
        chat_id = message.chat.id
        if chat_id not in pending_push_file:
            bot.reply_to(message, "Please use /push filename.py first before uploading a file.")
            return

        expected_filename = pending_push_file[chat_id]
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(expected_filename, 'wb') as f:
            f.write(downloaded_file)

        success = push_to_github(expected_filename)
        if success:
            bot.reply_to(message, f"{expected_filename} pushed to GitHub.")
        else:
            bot.reply_to(message, f"Failed to push {expected_filename}.")

        del pending_push_file[chat_id]
    except Exception as e:
        bot.reply_to(message, f"Error during push: {str(e)}")

@bot.message_handler(func=lambda m: True)
def default_response(message):
    bot.reply_to(message, "Smith is online. Use /push filename.py to upload and update a file.")

bot.infinity_polling()
