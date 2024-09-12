import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from rate import convert




# This part is responsible for logging so we wouldnt skip code errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


while True:
 # Start command.

    AMOUNT, CURRENCY1, CURRENCY2, EXCHANGE, START = range(5)




    async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
            global amount1
            amount1 = update.message.text
            print(amount1)
            try:
                amount1 = int(amount1)
                await update.message.reply_text('Now write the currency (e.g. usd, gel, eur)')
                amount1 = str(amount1)
                return AMOUNT
            except Exception: 
                await update.message.reply_text("Error, write just the amount.") 
                await amount(Update, ContextTypes.DEFAULT_TYPE)
                


    async def currency1(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        
        global currency_1
        currency_1 = update.message.text

        currency_1 = currency_1.strip().upper()
        print(currency_1)
        currency_1 = str(currency_1)
        try:
            if len(currency_1) == 3:
                await update.message.reply_text ('Write the currency you want ' + amount1 + currency_1 + ' in')
                return CURRENCY1
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception:
            await update.message.reply_text("Error, try again through /exchange")
            await exchange(Update, ContextTypes.DEFAULT_TYPE)
        
        
    async def currency2(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        global currency_2
        currency_2 = update.message.text
       
        currency_2 = currency_2.strip().upper()
        print(currency_2)
        currency_2 = str(currency_2)
        try:
            if len(currency_2) == 3:
                    finalresult = convert(amount1, currency_1, currency_2)
                    finalresult = str(finalresult)
                    await update.message.reply_text('Your rate for ' +amount1+currency_1 + ' = '+ finalresult+ currency_2+ '.\n\n\n\nThank you for using my service! \nType anything to proceed!\n\nCredits: @andrinoff')
                    return CURRENCY2
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception:
            await update.message.reply_text("Error, try again through /exchange")
            await exchange(Update, ContextTypes.DEFAULT_TYPE)

        
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text='Hello, ' + user.first_name  + '! \n Use "/exchange" to see exchange \n\n Credits:\n @andrinoff')
        amount1 = None
        currency_1 = None
        currency_2 = None
        return
    async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
        amount1 = None
        currency_1 = None
        currency_2 = None
        await update.message.reply_text('Write AMOUNT (e.g. 20)')

                
        return EXCHANGE


    if __name__ == '__main__':
        application = ApplicationBuilder().token('7307380567:AAHrnAsxUxwlg7cXWGjFvwlBS_NmoyirJ4I').build()

        start_handler = CommandHandler('start', start)
        
        exchange_handler = ConversationHandler(
            entry_points= [CommandHandler('exchange', exchange)],
                                        states = {
                                            EXCHANGE: [
                                                MessageHandler(filters.TEXT, amount),
                                                
                                            ],
                                            AMOUNT: [
                                                MessageHandler(filters.TEXT, currency1),
                                                
                                            ],
                                            CURRENCY1: [
                                                MessageHandler(filters.TEXT, currency2),
                                               
                                            ],
                                            CURRENCY2: [
                                                 MessageHandler(filters.TEXT, exchange)
                                            ],
                                            START: [
                                                 MessageHandler(filters.TEXT, exchange)
                                            ]
                                        },
                                        fallbacks= [CommandHandler("exchange", exchange)],
        )
        application.add_handler(start_handler)
        application.add_handler(exchange_handler)
        application.run_polling()
