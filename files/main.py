import logging
from math import isfinite
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, Updater
from rate import convert, check
from decimal import Decimal
from database import LanguageDatabase
from keys  import main, test, admin_password
from languagepack import translate
from amount import convert_amount

d = LanguageDatabase()

# Constants
ADMIN_KEY = "admin"

# This part is responsible for logging so we wouldnt skip code errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

administrators = ["andrinoff"]

# Error report function, write in the file, with userid, username, error
def errorreport(errors, user_id, name, language):
    errorlist = open('errors.txt', "a")
    errorlist.write(user_id, " AKA ", name, " encountered an error: ", errors, ". Language -- ", language)
    errorlist.close()

AMOUNT, CURRENCY1, CURRENCY2, EXCHANGE, ERROR = range(5)

# 2nd part of the conversation
# Gets the message about amount
# Verifies that amount is only made of numbers, not equal infinity nor NaN
# Stores in context memory with each user having their own
async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount1 = str(update.message.text)

        try:
            context.user_data["amount"] = convert_amount(amount1)

            await update.message.reply_text(translate(context.user_data["language"], "currency1"))

            return CURRENCY1
        except ValueError:
            await update.message.reply_text(translate(context.user_data["language"], "amounterror"))

            return AMOUNT

    except Exception as e:
        context.user_data['error'] = e
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
        context.user_data["currency2"] = currency_2
        currency_2 = str(currency_2)
        name = check (currency_2)
        if name == True:
            try:
                if len(currency_2) == 3:
                        finalresult = convert(Decimal(context.user_data["amount"]), str(context.user_data["currency1"]), str(context.user_data["currency2"]))
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
    errorreport(context.user_data['error'], update.message.chat.id, update.effective_user.full_name, context.user_data['language'])

    del context.user_data['amount']
    del context.user_data['currency1']
    del context.user_data['currency2']

    return EXCHANGE

# 1st part of the conversation
# Just sends the starting message
async def exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        try:
            language = d.get_user_language(update.message.chat.id)
            context.user_data['language'] = ''.join(["".join(lang) for lang in language])
        except:
            context.user_data["language"] = 'eng'
        context.user_data['amount']= None
        context.user_data['currency1'] = None
        context.user_data['currency2'] = None
        await update.message.reply_text(translate(context.user_data["language"], "amount"))
        return AMOUNT
    except Exception as e:
        return ERROR

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(translate(context.user_data["language"], "stop"))
    return ConversationHandler.END
# Commands to set a language
# Puts into the database the username + language

def language_func(language_id: str, welcome_message:str):
    async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            d.set_user_language(update.message.chat.id, language_id)
            await update.message.reply_text(welcome_message)
            context.user_data["language"] = language_id
            return EXCHANGE
        except:
            pass

    return language

#  Start command
# Quick tour through the bot usage
# Has a mechanism that checks if the user is registered in the system, if is, types the message in the language user is connected to
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        language = d.get_user_language(update.message.chat.id)
        context.user_data['language'] = ''.join(["".join(lang) for lang in language])
    except:
        context.user_data["language"] = 'eng'
    await update.message.reply_text(translate(context.user_data["language"], "start"), parse_mode="HTML")

async def credits(update:Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        language = d.get_user_language(update.message.chat.id)
        context.user_data['language'] = ''.join(["".join(lang) for lang in language])
    except:
        context.user_data["language"] = 'eng'

    await update.message.reply_text(translate(context.user_data["language"], "credits"), parse_mode="HTML")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username in administrators:
        await context.bot.delete_message(update.message.chat_id, update.message.message_id)
        context.user_data[ADMIN_KEY] = True
        await update.message.reply_text('You are logged in')
    else:
        password = str("".join(context.args))
        print(password)
        if password == admin_password:
            await context.bot.delete_message(update.message.chat_id, update.message.message_id)
            context.user_data[ADMIN_KEY] = False
            await update.message.reply_text("You are currently logged in")
        else:
            await context.bot.delete_message(update.message.chat_id, update.message.message_id)
            context.user_data[ADMIN_KEY] = False
            await update.message.reply_text("You don't have the administrator rights")

async def sendall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(ADMIN_KEY, False):
        await update.message.reply_text("You are not an admin")

        return

    msg = "".join(context.args)

    for chat_id in d.client_list():
        try:
            await context.bot.send_message(chat_id, msg)
        except Exception as e:
            logging.error(f"Failed to send message to {chat_id}: {e}")

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    del context.user_data[ADMIN_KEY]

    update.message.reply_text('You logged out successfully, ', update.effective_user.name)

# If that always works
# Insert token into the program
# Creates conversation handler
# makes /exchange the start of the conversation
#  Adds states
# Adds the conversation handler to the working bot
# Runs the bot
if __name__ == '__main__':
    # application = ApplicationBuilder().token(main).build()
    application = ApplicationBuilder().token(test).build()
    exchange_handler = ConversationHandler(
        entry_points=[CommandHandler('exchange', exchange)],
        states={
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
            ],
        },
        fallbacks=[CommandHandler("stop", stop),
                    MessageHandler(filters.COMMAND, exchange)],
    )
    application.add_handler(exchange_handler)

    for name, handlerFunc in [
            ("rus", language_func("rus", "Успешно изменен язык!")),
            ("eng", language_func("eng", "Language set successfully!")),
            ("ukr", language_func("ukr", "Мову встановлено успішно!")),
            ("kar", language_func("kar", "ენა გადმოწერილია")),
            ("start", start), ("credits", credits), ("admin", admin), ("sendall", sendall),
        ]:
        application.add_handler(CommandHandler(name, handlerFunc))

    application.run_polling()
