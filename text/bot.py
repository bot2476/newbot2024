import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# টেলিগ্রাম বট টোকেন দিন
API_TOKEN = '7532229468:AAHBHCFYkkRqocFfgwicxAdOUthD-3Ht6NU'
CHANNEL_USERNAME = '@hy78oj'  # Replace with the correct channel username

bot = telebot.TeleBot(API_TOKEN)

# মুভি ডাটাবেস (আপডেট করুন নিজের মতো করে)
movies = {
    "titanic": "🎥 *Titanic* (1997)\n🔗 [Watch Now](https://t.me/hy78oj/123)",
    "avatar": "🎥 *Avatar* (2009)\n🔗 [Watch Now](https://t.me/hy78oj/124)",
    "inception": "🎥 *Inception* (2010)\n🔗 [Watch Now](https://t.me/hy78oj/125)"
}

# /start কমান্ড
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🎬 Welcome to the Movie Bot!\n\n"
        "➡️ To use this bot, you need to join our channel first.\n\n"
        "🔸 Join and click the 'Verify Now' button below to proceed."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
    markup.add(InlineKeyboardButton("✅ Verify Now", callback_data="verify"))
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ভেরিফিকেশন প্রক্রিয়া
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_user(call):
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, call.from_user.id).status
        if user_status in ['member', 'administrator', 'creator']:
            bot.answer_callback_query(call.id, "✅ Verification successful!")
            bot.send_message(call.message.chat.id, (
                "✅ You are verified!\n\n"
                "📖 *How to search for movies:*\n"
                "Type `/search <movie name>` to find your desired movie.\n\n"
                "*Example:*\n"
                "`/search Titanic`"
            ), parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "⚠️ You are not in the channel yet. Please join the channel first.")
    except Exception as e:
        print(f"Error: {e}")
        bot.answer_callback_query(call.id, "⚠️ Unable to verify. Make sure you've joined the channel.")

# /search কমান্ড
@bot.message_handler(commands=['search'])
def search_movie(message):
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        bot.reply_to(message, "❌ Please provide a movie name. Example: `/search Titanic`", parse_mode="Markdown")
        return

    movie_name = query[1].lower()
    if movie_name in movies:
        bot.reply_to(message, movies[movie_name], parse_mode="Markdown")
    else:
        bot.reply_to(message, f"❌ Sorry, no results found for '{movie_name}'. Please try another movie.", parse_mode="Markdown")

# বট চালু করুন
print("🤖 Bot is running...")
bot.infinity_polling()
