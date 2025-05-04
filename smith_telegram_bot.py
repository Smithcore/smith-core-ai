
import os
import telebot
from openai import OpenAI

# Load tokens from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize bot and OpenAI
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# Handle any text message like natural conversation
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Smith, an elite AI assistant. Speak like a strategist, think like an executor."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"[Smith Error: {str(e)}]")

# Start polling
bot.polling()
