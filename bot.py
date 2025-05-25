import telebot
from telebot.types import ReplyKeyboardMarkup
from datetime import datetime

# ==== BOT CONFIG ====
BOT_TOKEN = "7660535947:AAECOgdeu_RUJt7nKXVs7F7suYLqw8bw8sQ"  # Replace with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

# ==== FILES TO SAVE ====
CONTACTS_FILE = "contacts.txt"
MESSAGES_FILE = "messages.txt"

# ==== SHLOKS LIST ====
shloks_list = [
    {
        "shlok": "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय।",
        "meaning": "Perform your duties with dedication and detachment.",
        "context": "This teaches us the spirit of selfless action."
    },
    {
        "shlok": "न जायते म्रियते वा कदाचि‍त्...",
        "meaning": "The soul is never born, nor does it die.",
        "context": "It speaks about the eternal nature of the soul."
    },
    {
        "shlok": "पत्रं पुष्पं फलं तोयं यो मे भक्त्या प्रयच्छति।",
        "meaning": "If one offers Me a leaf, a flower, fruit or water with devotion, I accept it.",
        "context": "God values devotion more than material offerings."
    },
    {
        "shlok": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।",
        "meaning": "You have the right to perform your prescribed duties, but never to the results.",
        "context": "Focus on actions, not the fruits."
    }
]

# ==== USER STATES ====
user_states = {}

# ==== START COMMAND ====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_states[user_id] = {"stage": "ask_name"}
    bot.send_message(user_id, "Namaste! Welcome to Satya Sampatti Shlok Bot.\nMay I know your name?")

# ==== HANDLE ALL TEXT ====
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.chat.id
    text = message.text.strip().lower()

    if user_id not in user_states:
        user_states[user_id] = {"stage": "ask_name"}
        bot.send_message(user_id, "May I know your name?")
        return

    state = user_states[user_id]

    # Stage 1: Ask Name
    if state["stage"] == "ask_name":
        state["name"] = message.text.strip()
        state["stage"] = "ask_contact"
        bot.send_message(user_id, f"Thank you, {state['name']}! Please share your contact number or email:")
        return

    # Stage 2: Ask Contact
    elif state["stage"] == "ask_contact":
        state["contact"] = message.text.strip()
        state["stage"] = "complete"
        state["shlok_index"] = 0
        with open(CONTACTS_FILE, "a") as f:
            f.write(f"{datetime.now()} | Name: {state['name']} | Contact: {state['contact']} | Telegram ID: {user_id}\n")

        bot.send_message(
            user_id,
            f"Welcome, {state['name']}!\nI am your Shlok Guide.\n\n"
            f"You can type `karma`, `atman`, or `bhakti` to get a specific shlok,\n"
            f"or type `more` to get a random shlok.\n\n"
            f"To stop, just type `stop`.",
            parse_mode='Markdown'
        )
        return

    # Stage 3: Provide shlok
    elif state["stage"] == "complete":
        with open(MESSAGES_FILE, "a") as f:
            f.write(f"{datetime.now()} | {state['name']} ({user_id}): {message.text.strip()}\n")

        if text == "stop":
            bot.send_message(
                user_id,
                "Thank you for exploring the wisdom of the Gita.\nWould you like to read high-quality blogs on earning, health, or spirituality?\nVisit: https://satyasampatti.com"
            )
            return

        elif text == "more":
            idx = state.get("shlok_index", 0)
            if idx < len(shloks_list):
                s = shloks_list[idx]
                response = (
                    f"*Shlok:*\n{s['shlok']}\n\n"
                    f"*Meaning:*\n{s['meaning']}\n\n"
                    f"*Context:*\n{s['context']}"
                )
                bot.send_message(user_id, response, parse_mode='Markdown')
                state["shlok_index"] += 1
                if state["shlok_index"] < len(shloks_list):
                    bot.send_message(user_id, "If you want more, type 'more'. To stop, type 'stop'.")
                else:
                    bot.send_message(user_id, "That was the last shlok. To explore more, visit https://satyasampatti.com")
            else:
                bot.send_message(user_id, "All shloks have been shared. You can now explore our blog at https://satyasampatti.com")
            return

        elif text in ["karma", "atman", "bhakti"]:
            keyword_map = {
                "karma": 0,
                "atman": 1,
                "bhakti": 2
            }
            index = keyword_map[text]
            s = shloks_list[index]
            response = (
                f"*Shlok:*\n{s['shlok']}\n\n"
                f"*Meaning:*\n{s['meaning']}\n\n"
                f"*Context:*\n{s['context']}"
            )
            bot.send_message(user_id, response, parse_mode='Markdown')
            state["shlok_index"] = index + 1
            if state["shlok_index"] < len(shloks_list):
                bot.send_message(user_id, "If you want more, type 'more'. To stop, type 'stop'.")
            else:
                bot.send_message(user_id, "That was the last shlok. To explore more, visit https://satyasampatti.com")
            return

        else:
            bot.send_message(user_id, "Please type a keyword like `karma`, or type `more` for a random shlok.", parse_mode='Markdown')

# ==== START BOT ====
print("Bot is running...")
bot.infinity_polling()
