import logging
import yfinance as yf
from telegram import Update
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
    'TSM': 'TSMC',     # Taiwan Semiconductor
    'IBM': 'IBM',
    
    # International Tech
    'BABA': 'Alibaba', # China
    'SONY': 'Sony',    # Japan
    'SAP': 'SAP'       # Germany
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
        # fast_info is generally faster and more reliable for real-time fetch
        price = stock.fast_info['last_price']
        return price
    except Exception:
        return None

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user}! 🤖\n\n"
        "I am your upgraded Tech Stock Bot.\n\n"
        "**Commands:**\n"
        "/tech - View prices for 18+ major global tech companies\n"
        "/price <SYMBOL> - Check any specific stock (e.g., /price BTC-USD)"
    )

async def tech_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📉 Fetching data for global tech market...")
    
    # Create a formatted message
    message_lines = ["**🌍 Global Tech Market Update**\n"]
    
    # Loop through the dictionary
    for symbol, name in TECH_STOCKS.items():
        price = get_live_price(symbol)
        if price:
            # Add an emoji based on the stock grouping or just a generic bullet
            message_lines.append(f"• **{name} ({symbol})**: ${price:.2f}")
        else:
            message_lines.append(f"• {name}: ⚠️ Error")
            
    # Send the long message
    await update.message.reply_text("\n".join(message_lines), parse_mode='Markdown')

async def check_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/price TSLA`", parse_mode='Markdown')
        return

    symbol = context.args[0].upper()
    status_msg = await update.message.reply_text(f"🔍 Checking {symbol}...")
    price = get_live_price(symbol)
    
    if price:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"📊 **{symbol}**: ${price:.2f}",
            parse_mode='Markdown'
        )
    else:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=status_msg.message_id,
            text=f"❌ Could not find symbol **{symbol}**.",
            parse_mode='Markdown'
        )

# --- MAIN ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('tech', tech_summary))
    application.add_handler(CommandHandler('price', check_price))
    
    print("Bot is starting with expanded stock list...")
    application.run_polling()
