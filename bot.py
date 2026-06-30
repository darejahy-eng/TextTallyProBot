import os
import re
import logging
from telebot import TeleBot, types

# Setup logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get bot token from environment variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
    exit(1)

bot = TeleBot(BOT_TOKEN)

# Store user data (temporary - reset on restart)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command"""
    welcome_text = """
📊 **Welcome to TextTallyProBot!**

I'm your intelligent text analysis assistant. I can analyze any text you send me.

**Available Commands:**
📝 `/word_count` - Count words and characters
📄 `/sentence_count` - Count sentences and paragraphs  
📊 `/full_analysis` - Complete text breakdown
📈 `/stats` - Detailed text statistics
❓ `/help` - Show this message again

**Quick Tip:** Just send me any text and I'll auto-analyze it!
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    logger.info(f"User {message.from_user.id} started the bot")

@bot.message_handler(commands=['help'])
def send_help(message):
    """Handle /help command"""
    help_text = """
📚 **Help - Available Commands**

🔹 `/start` - Welcome message with bot introduction
🔹 `/help` - Show this help message
🔹 `/word_count` - Count words, characters (with/without spaces)
🔹 `/sentence_count` - Count sentences and paragraphs
🔹 `/full_analysis` - Complete analysis (words, chars, sentences, paragraphs)
🔹 `/stats` - Detailed statistics (unique words, avg length)

**How to Use:**
1. Type a command (e.g., `/word_count`)
2. Send the text you want to analyze
3. I'll reply with the analysis!

**Example:**
`/word_count` → then send "Hello world!" → I'll show word count
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['word_count'])
def word_count_command(message):
    """Handle /word_count command"""
    msg = bot.reply_to(message, "📝 Please send the text you want to analyze.")
    bot.register_next_step_handler(msg, process_word_count)

def process_word_count(message):
    """Process word count request"""
    try:
        text = message.text
        words = len(text.split())
        chars = len(text)
        chars_no_space = len(text.replace(" ", ""))
        
        response = f"""
📊 **Word Count Analysis**

📝 **Words:** {words}
🔠 **Characters (with spaces):** {chars}
🔡 **Characters (no spaces):** {chars_no_space}
"""
        bot.reply_to(message, response, parse_mode='Markdown')
        logger.info(f"Word count processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in word_count: {e}")
        bot.reply_to(message, "⚠️ Error analyzing text. Please try again.")

@bot.message_handler(commands=['sentence_count'])
def sentence_count_command(message):
    """Handle /sentence_count command"""
    msg = bot.reply_to(message, "📄 Please send the text to count sentences.")
    bot.register_next_step_handler(msg, process_sentence_count)

def process_sentence_count(message):
    """Process sentence count request"""
    try:
        text = message.text
        # Count sentences by splitting on . ! ?
        sentences = len(re.split(r'[.!?]+', text)) - 1
        sentences = max(0, sentences)
        # Count paragraphs by double newline
        paragraphs = len(text.split('\n\n')) if '\n\n' in text else 1
        
        response = f"""
📄 **Sentence & Paragraph Count**

📝 **Sentences:** {sentences}
📑 **Paragraphs:** {paragraphs}
"""
        bot.reply_to(message, response, parse_mode='Markdown')
        logger.info(f"Sentence count processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in sentence_count: {e}")
        bot.reply_to(message, "⚠️ Error analyzing text. Please try again.")

@bot.message_handler(commands=['full_analysis'])
def full_analysis_command(message):
    """Handle /full_analysis command"""
    msg = bot.reply_to(message, "🔍 Please send the text for complete analysis.")
    bot.register_next_step_handler(msg, process_full_analysis)

def process_full_analysis(message):
    """Process full analysis request"""
    try:
        text = message.text
        words = len(text.split())
        chars = len(text)
        sentences = len(re.split(r'[.!?]+', text)) - 1
        sentences = max(0, sentences)
        paragraphs = len(text.split('\n\n')) if '\n\n' in text else 1
        avg_words_per_sentence = words / sentences if sentences > 0 else 0
        
        response = f"""
📊 **Complete Text Analysis**

📝 **Words:** {words}
🔠 **Characters:** {chars}
📄 **Sentences:** {sentences}
📑 **Paragraphs:** {paragraphs}
📋 **Avg Words/Sentence:** {avg_words_per_sentence:.1f}
"""
        bot.reply_to(message, response, parse_mode='Markdown')
        logger.info(f"Full analysis processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in full_analysis: {e}")
        bot.reply_to(message, "⚠️ Error analyzing text. Please try again.")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    """Handle /stats command"""
    msg = bot.reply_to(message, "📊 Please send the text for detailed statistics.")
    bot.register_next_step_handler(msg, process_stats)

def process_stats(message):
    """Process detailed statistics request"""
    try:
        text = message.text
        words = text.split()
        word_count = len(words)
        unique_words = len(set(words))
        avg_word_len = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        chars = len(text)
        sentences = len(re.split(r'[.!?]+', text)) - 1
        sentences = max(0, sentences)
        paragraphs = len(text.split('\n\n')) if '\n\n' in text else 1
        
        response = f"""
📊 **Detailed Statistics**

📝 **Total Words:** {word_count}
🆕 **Unique Words:** {unique_words}
📏 **Avg Word Length:** {avg_word_len:.1f}
🔡 **Total Characters:** {chars}
📄 **Sentences:** {sentences}
📑 **Paragraphs:** {paragraphs}
"""
        bot.reply_to(message, response, parse_mode='Markdown')
        logger.info(f"Detailed stats processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in stats: {e}")
        bot.reply_to(message, "⚠️ Error analyzing text. Please try again.")

@bot.message_handler(func=lambda message: True)
def auto_analyze(message):
    """Auto-analyze any text sent to the bot"""
    try:
        text = message.text
        words = len(text.split())
        characters = len(text)
        
        response = f"""
📝 **Quick Analysis**

📊 **Words:** {words}
🔠 **Characters:** {characters}

💡 Use `/full_analysis` for complete breakdown.
"""
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in auto_analyze: {e}")

# Health check endpoint for Railway (optional)
@bot.message_handler(commands=['health'])
def health_check(message):
    """Simple health check command"""
    bot.reply_to(message, "✅ Bot is running smoothly!")

if __name__ == "__main__":
    logger.info("🤖 TextTallyProBot is starting...")
    try:
        # Start the bot with infinity polling for Railway
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        exit(1)
