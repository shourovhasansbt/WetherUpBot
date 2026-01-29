import logging
import yfinance as yf
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CONFIGURATION ---
# ⚠️ SECURITY WARNING: You posted this token publicly. 
# It is highly recommended to revoke this and generate a new one via @BotFather.
TOKEN = '8542597972:AAEIr1EV2RWSC4j4GqO8xVm_PG3qYycrD88'

# EXPANDED List of World Tech Companies
TECH_STOCKS = {
    # Big 7
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOGL': 'Google',
    'AMZN': 'Amazon',
    'TSLA': 'Tesla',
    'NVDA': 'Nvidia',
    'META': 'Meta',
    
    # Major Software & Internet
    'NFLX': 'Netflix',
    'ADBE': 'Adobe',
    'CRM': 'Salesforce',
    'ORCL': 'Oracle',
    'SPOT': 'Spotify',
    'UBER': 'Uber',
    
    # Hardware & Semiconductors
    'AMD': 'AMD',
    'INTC': 'Intel',
    'TSM': 'TSMC',
    'IBM': 'IBM',
    
    # International Tech
    'BABA': 'Alibaba', 
    'SONY': 'Sony',
    'SAP': 'SAP'
}

# --- LOGGING SETUP ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- HELPER FUNCTION ---
def get_live_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        price = stock.fast_info['last_price']
        return price
    except Exception:
        return None

# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user}! 🤖\n\n"
        "I am your **World Tech Stock Bot**.\n"
        "I provide live updates on major global tech companies.\n\n"
        "**Available Commands:**\n"
        "📈 /tech - View prices for 18+ major tech giants\n"
        "💰 /price <SYMBOL> - Check specific stock (e.g., /price BTC-USD)\n"
        "👨‍💻 /developer - About the creator\n\n"
        "_Bot by Mohammad Shourov_",
        parse_mode=ParseMode.MARKDOWN
    )

async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays developer information."""
    dev_info = (
        "**👨‍💻 About the Developer**\n\n"
        "**Name:** Mohammad Shourov\n\n"
        "**🌐 Socials:**\n"
        "• [Facebook](https://www.facebook.com/share/1KZZpxp28P/)\n"
        "• [GitHub](https://github.com/shourovhasansbt)\n"
        "• [Instagram](https://instagram.com/mohammadshourov01)\n"
        "• [Telegram](https://t.me/mohammadshourov0011)\n\n"
        "_Feel free to contact for inquiries!_"
    )
    # disable_web_page_preview=True prevents the big Facebook preview image from cluttering the chat
    await update.message.reply_text(dev_info, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def tech_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📉 Fetching data for global tech market...")
    
    message_lines = ["**🌍 Global Tech Market Update**\n"]
    
    for symbol, name in TECH_STOCKS.items():
        price = get_live_price(symbol)
        if price:
            message_lines.append(f"• **{name} ({symbol})**: ${price:.2f}")
        else:
            message_lines.append(f"• {name}: ⚠️ Error")
            
    message_lines.append("\n_Bot by Mohammad Shourov_")
    await update.message.reply_text("\n".join(message_lines), parse_mode=ParseMode.MARKDOWN)

async def check_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/price TSLA`", parse_mode=ParseMode.MARKDOWN)
        return

    symbol = context.args[0].upper()
    status_msg = await update.message.reply_text(f"🔍 Checking {symbol}...")
    price = get_live_price(symbol)
    
    if price:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"📊 **{symbol}**: ${price:.2f}\n\n_Bot by Mohammad Shourov_",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"❌ Could not find symbol **{symbol}**.",
            parse_mode=ParseMode.MARKDOWN
        )

# --- MAIN ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('tech', tech_summary))
    application.add_handler(CommandHandler('price', check_price))
    application.add_handler(CommandHandler('developer', developer))
    
    print("Bot is starting... (Creator: Mohammad Shourov)")
    application.run_polling()
