import logging
from math import isfinite
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from rate import convert
import decimal

from decimal import Decimal


# This part is responsible for logging so we wouldnt skip code errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 
while True:
    def errorreport(errors, user_id, user_name):
        errorlist = open('errors.txt', "a")
        errorlist.write(user_id, " AKA ", user_name, " encounted an error: ", errors)
        errorlist.close()
    AMOUNT, CURRENCY1, CURRENCY2, EXCHANGE, ERROR = range(5)
    
    
    async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            amount1 = update.message.text
            print(amount1)
            context.user_data["amount"] = decimal(amount1)
            try:
                int(amount1)
            except ValueError:
                await update.message.reply_text ('Write the number')
                return AMOUNT
            context.user_data["amount"] = Decimal(str(amount1))
            print (context.user_data["amount"])
            print (isfinite(context.user_data["amount"]))
            if isfinite(context.user_data["amount"]) == True:
                try:
                    await update.message.reply_text('Now write the currency (e.g. usd, gel, eur)')
                    return CURRENCY1
                except ValueError: 
                    await update.message.reply_text("Error, write just the amount.") 
                    return ERROR
            else: 
                await update.message.reply_text("You can't use infinity, nor NaN")
                return AMOUNT
        except Exception as e:
            context.user_data['error'] = e
            return ERROR
    async def currency1(update: Update, context: ContextTypes.DEFAULT_TYPE):
        currency_1 = update.message.text
        currency_1 = currency_1.strip().upper()
        print(currency_1)
        context.user_data["currency1"] = currency_1

        currency_1 = str(currency_1)
        try:
            if len(currency_1) == 3:
                await update.message.reply_text ('Write the currency you want ' + str(context.user_data["amount"]) + context.user_data['currency1'] + ' in')
                return CURRENCY2
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception as e:
            context.user_data['error'] = e
            return ERROR

        
    async def currency2(update: Update, context: ContextTypes.DEFAULT_TYPE):
        currency_2 = update.message.text
        currency_2 = currency_2.strip().upper()
        print(currency_2)
        context.user_data["currency2"] = currency_2
        currency_2 = str(currency_2)
        try:
            if len(currency_2) == 3:
                    finalresult = convert(Decimal(context.user_data["amount"]), str(context.user_data["currency1"]), str(context.user_data["currency2"]))
                    print(finalresult)
                    finalresult = str(finalresult)
                    await update.message.reply_text('Your rate for ' +str(context.user_data["amount"])+context.user_data["currency1"] + ' = '+ str(finalresult)+ context.user_data["currency1"]+ '.\n\n\n\nThank you for using my service! \nType anything to proceed!\n\nCredits: @andrinoff')
                    return EXCHANGE
            else:
                await update.message.reply_text("Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)") 
        except Exception as e:
            context.user_data['error'] = e
            return ERROR

        
    async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text ('An error encounted, reported \n You will start over')
        errorreport(context.user_data['errors'], context._user_id,update.effective_user.username)
        context.user_data['amount'] = None
        context.user_data['currency1']  = None
        context.user_data['currency2']  = None
        return EXCHANGE
    async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            context.user_data['amount']= None
            context.user_data['currency1'] = None
            context.user_data['currency2'] = None
            await update.message.reply_text('Write AMOUNT (e.g. 20)')         
            return AMOUNT
        except:
            return ERROR

    if __name__ == '__main__':
        application = ApplicationBuilder().token('7307380567:AAHrnAsxUxwlg7cXWGjFvwlBS_NmoyirJ4I').build()     
        # application = ApplicationBuilder().token('6993319781:AAGPkkgWZARSMSc94FBIw9vYZ-e09eyTqoM').build()       
        exchange_handler = ConversationHandler(
            entry_points= [CommandHandler('exchange', exchange)],
                                        states = {
                                            AMOUNT: [
                                                MessageHandler(filters.TEXT, amount),
                                                
                                            ],
                                            CURRENCY1: [
                                                MessageHandler(filters.TEXT, currency1),
                                                
                                            ],
                                            CURRENCY2: [
                                                MessageHandler(filters.TEXT, currency2),
                                               
                                            ],
                                            EXCHANGE: [
                                                 MessageHandler(filters.TEXT, exchange)
                                            ],
                                            ERROR: [
                                                 MessageHandler(filters.TEXT, error)
                                            ]
                                        },
                                        fallbacks= [CommandHandler("exchange", exchange)],
        )
        application.add_handler(exchange_handler)
        application.run_polling()