import logging
from math import isfinite
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, Updater
from rate import convert, check
import decimal
from decimal import Decimal
import database as d
from keys  import main, test
from languagepack import ukr, eng, rus, translate

d.__init__()

# This part is responsible for logging so we wouldnt skip code errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



# Error report function, write in the file, with userid, username, error
def errorreport(errors, user_id, user_name):
    errorlist = open('errors.txt', "a")
    errorlist.write(user_id, " AKA ", user_name, " encounted an error: ", errors)
    errorlist.close()

AMOUNT, CURRENCY1, CURRENCY2, EXCHANGE, ERROR = range(5)

# 2nd part of the conversation
# Gets the message about amount
# Verifies that amount is only made of numbers, not equal infinity nor NaN
# Stores in context memory with each user having their own
async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount1 = update.message.text
        print(amount1)
        print('went through 2')
        amount1 = str(amount1)
        if "." in amount1:
            amountcheck = amount1.replace(".", "")
            if amountcheck.isnumeric() == False:
                await update.message.reply_text(translate(context.user_data["language"], "amounterror"))
                return AMOUNT 
            else: 
                context.user_data["amount"] = Decimal(str(amount1))
                print (context.user_data["amount"])
                print (isfinite(context.user_data["amount"]))
                if isfinite(context.user_data["amount"]) == True:
                    try:
                        await update.message.reply_text(translate(context.user_data["language"], "currency1"))
                        return CURRENCY1
                    except ValueError: 
                        await update.message.reply_text(translate(context.user_data["language"], "amounterror")) 
                        return ERROR
                else: 
                        await update.message.reply_text(translate(context.user_data["language"], "amounterror"))
                        return AMOUNT
        else:
                if amount1.isnumeric() == False:
                    await update.message.reply_text(translate(context.user_data["language"], "amounterror"))
                    return AMOUNT 
                else: 
                    context.user_data["amount"] = Decimal(str(amount1))
                    print (context.user_data["amount"])
                    print (isfinite(context.user_data["amount"]))
                    if isfinite(context.user_data["amount"]) == True:
                        try:
                            await update.message.reply_text(translate(context.user_data["language"], "currency1"))
                            return CURRENCY1
                        except ValueError: 
                            await update.message.reply_text(translate(context.user_data["language"], "amounterror")) 
                            return ERROR
                    else: 
                            await update.message.reply_text(translate(context.user_data["language"], "amounterror"))
                            return AMOUNT
    except Exception as e:
        context.user_data['error'] = e
        print(e)
        return ERROR
    
# 3rd part of the conversation
# Gets the message about 1st currency
# Makes all letter capitals and removes whitespaces
# Checks if the currency is in the dict with all the currencies
# Checks if the currency is made out of 3 letters
# Error handler, throwback to the start when needed
async def currency1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency_1 = update.message.text
    currency_1 = currency_1.strip().upper()
    if currency_1.isalpha() == True:
        name = check(currency_1)
        if name == True:
            print(currency_1)
            context.user_data["currency1"] = currency_1
            currency_1 = str(currency_1)
            try:
                if len(currency_1) == 3:
                    await update.message.reply_text (translate(context.user_data["language"], "currency2.1") + str(context.user_data["amount"]) + context.user_data['currency1'] + translate(context.user_data["language"], "currency2.2"))
                    return CURRENCY2
                else:
                    await update.message.reply_text(translate(context.user_data["language"], "currencyerror1")) 
            except Exception as e:
                context.user_data['error'] = e
                return ERROR
        else:
            await update.message.reply_text(translate(context.user_data["language"], "currencyerror2"))
            return CURRENCY1
    else:
        await update.message.reply_text(translate(context.user_data["language"], "currencyerror1"))
        return CURRENCY1
    
# 4th part of the conversation
# Gets the message
# Checks if the currency is real
# Checks if the currency is out of only 3 letters
# Calculates and gives the result
# Goes back to the start
async def currency2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency_2 = update.message.text
    currency_2 = currency_2.strip().upper()
    if currency_2.isalpha() == True:
        print(currency_2)
        context.user_data["currency2"] = currency_2
        currency_2 = str(currency_2)
        name = check (currency_2)
        if name == True:
            try:
                if len(currency_2) == 3:
                        finalresult = convert(Decimal(context.user_data["amount"]), str(context.user_data["currency1"]), str(context.user_data["currency2"]))
                        print(finalresult)
                        if finalresult != False:
                            finalresult = str(finalresult)
                            await update.message.reply_text(translate(context.user_data["language"], "result.1") +str(context.user_data["amount"])+context.user_data["currency1"] + ' = '+ str(finalresult)+ context.user_data["currency2"]+ translate(context.user_data["language"], "result.2"))
                            return EXCHANGE
                        else:
                            await update.message.reply_text(translate(context.user_data["language"], "error"))
                            return EXCHANGE
                else:
                    await update.message.reply_text(translate(context.user_data["language"], "currencyerror1")) 
            except Exception as e:
                context.user_data['error'] = e
                return ERROR
        else:
            await update.message.reply_text(translate(context.user_data["language"], "currencyerror2"))
            return CURRENCY2
    else:
        await update.message.reply_text(translate(context.user_data["language"], "currencyerror1"))
        return CURRENCY2
    
# Error handler, in case of an error, saves the error in errors.txt
# Clears all the values
# Goes back to the start
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text (translate(context.user_data["language"], "error"))
    errorreport(context.user_data['errors'], context._user_id,update.effective_user.username)
    context.user_data['amount'] = None
    context.user_data['currency1']  = None
    context.user_data['currency2']  = None
    return EXCHANGE

# 1st part of the conversation
# Just sends the starting message
async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('exchange test0')
    try:
        print('exchange test1')
        language = d.findlanguage(update.effective_user.username)
        language = list(language)
        print(type(language))
        context.user_data['language'] = ''.join(["".join(lang) for lang in language])
        print("exchange test2")
        print (context.user_data['language'])
        context.user_data['amount']= None
        context.user_data['currency1'] = None
        context.user_data['currency2'] = None
        await update.message.reply_text(translate(context.user_data["language"], "amount"))         
        return AMOUNT
    except Exception as e:
        print(e)
        return ERROR
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(translate(context.user_data["language"], "stop"))
    return ConversationHandler.END
# Commands to set a language
# Puts into the database the username + language
async def rus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        d.addlanguage(update.effective_user.username, "rus")
        await update.message.reply_text('Успешно изменен язык!')
        return EXCHANGE
    except Exception as e:
        print(e)
async def eng(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        d.addlanguage(update.effective_user.username, "eng")
        await update.message.reply_text('Language set successfully!')
        return EXCHANGE
    except Exception as e:
        print(e)
async def ukr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print(update.effective_user.username)
        d.addlanguage(update.effective_user.username, "ukr")
        await update.message.reply_text('Мову встановлено успішно!')
        return EXCHANGE
    except Exception as e:
        print(e)
# If that always works
# Insert token into the program
# Creates converstation handler
# makes /exchange the start of the conversation
#  Adds states
# Adds the conversation handler to the working bot
# Runs the bot
if __name__ == '__main__':
    application = ApplicationBuilder().token(main).build()     
    # application = ApplicationBuilder().token(test).build() 
    rus_handler = CommandHandler("rus", rus)     
    eng_handler = CommandHandler("eng", eng)
    ukr_handler = CommandHandler("ukr", ukr) 
    exchange_handler = ConversationHandler(
        entry_points= [CommandHandler('exchange', exchange)],
                                    states = {
                                        AMOUNT: [
                                            MessageHandler(filters.TEXT & (~ filters.COMMAND), amount),
                                            
                                        ],
                                        CURRENCY1: [
                                            MessageHandler(filters.TEXT & (~ filters.COMMAND), currency1),
                                            
                                        ],
                                        CURRENCY2: [
                                            MessageHandler(filters.TEXT & (~ filters.COMMAND), currency2),
                                            
                                        ],
                                        EXCHANGE: [
                                                MessageHandler(filters.TEXT & (~ filters.COMMAND), exchange)
                                        ],
                                        ERROR: [
                                                MessageHandler(filters.TEXT & (~ filters.COMMAND), error)
                                        ]
                                    },
                                    fallbacks= [MessageHandler(filters.COMMAND, stop)],
    )

    application.add_handler(rus_handler)
    application.add_handler(eng_handler)
    application.add_handler(ukr_handler)
    application.add_handler(exchange_handler)
    application.run_polling()

