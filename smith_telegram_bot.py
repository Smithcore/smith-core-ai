import os
from dotenv import load_dotenv
import telebot
from github import Github

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # e.g., "username/reponame"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
github = Github(GITHUB_TOKEN)
repo = github.get_repo(GITHUB_REPO)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "SmithCore is online and listening.")

@bot.message_handler(commands=['pull'])
def pull_file(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /pull filename.py")
            return

        filename = parts[1]
        contents = repo.get_contents(filename)
        with open(filename, "w") as f:
            f.write(contents.decoded_content.decode())

        with open(filename, "rb") as f:
            bot.send_document(message.chat.id, f, visible_file_name=filename)

    except Exception as e:
        bot.reply_to(message, f"Pull failed: {str(e)}")

@bot.message_handler(commands=['push'])
def push_file(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Usage: /push filename.py")
            return

        filename = parts[1]
        with open(filename, "r") as f:
            content = f.read()

        github_file = repo.get_contents(filename)
        repo.update_file(github_file.path, f"Updated {filename}", content, github_file.sha)
        bot.reply_to(message, f"{filename} pushed to GitHub.")

    except Exception as e:
        bot.reply_to(message, f"Push failed: {str(e)}")

bot.polling()
