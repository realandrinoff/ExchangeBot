eng = {
    "amount": "Write AMOUNT (e.g. 20)",
    "amounterror": "Write just the amount",
    "currency1": "Now write the currency (e.g. usd, gel, eur)",
    "currencyerror1": "Error, write just the currency! (It has to be 3 letters long) (e.g USD, GEL)",
    "currencyerror2": "This currency isnt real, try again",
    "currency2.1": "Write the currency you want ",
    "currency2.2": " in",
    "result.1": 'Your rate for ',
    "result.2": ".\n\n\n\nThank you for using my service! \nType /exchange or anything to proceed!\n\nCredits: @andrinoff",
    "error": 'An error encounted, reported \n You will start over',
    "stop": "The bot was stopped. \n\n You can proceed anytime by /exchange"
}
ukr = {
    "amount": "Напишіть СУМУ (наприклад, 20)",
    "amounterror": "Напишіть тільки суму",
    "currency1": "Тепер напишіть валюту (наприклад, usd, gel, eur)",
    "currencyerror1": "Помилка, напишіть лише валюту! (Він має містити 3 літери) (наприклад, USD, GEL)",
    "currencyerror2": "Ця валюта несправжня, спробуйте ще раз",
    "currency2.1": "Напишіть валюту, у якій хочете отримати ",
    "currency2.2": "",
    "result.1": 'Ваша ставка для ',
    "result.2": ".\n\n\n\nДякую, що скористалися моїм сервісом! \nВведіть /exchange, щоб продовжити!\n\nТворець: @andrinoff",
    "error": 'Виявлено помилку, повідомлено\n Ви почнете спочатку',
    "stop": "Роботу бота було зупинено.\n\n Ви можете будь-коли продовжити за допомогою /exchange"

}
rus = {
    "amount": "Напишите кол-во (например, 20)",
    "amounterror": "Напишите ТОЛЬКО кол-во",
    "currency1": "Теперь, напишите валюту на английском(например, usd, gel, gbp)",
    "currencyerror1": "Ошибка, напишите только валюту (3 буквы)",
    "currencyerror2": "Эта валюта не существует",
    "currency2.1": "Напишите валюту вы хотите ",
    "currency2.2": " в",
    "result.1": 'Ваш курс для ',
    "result.2": ".\n\n\n\nСпасибо за использование! \n Напишите /exchange, чтобы продолжить\n\n Создатель: @andrinoff",
    "error": 'Ошибка! \n Вы начнете сначала',
    "stop": "Вы остановили бота. \n\n Вы можете продолжить, когда хотите с /exchange"
}

def translate(language, step):
    if language == "ukr":
        phrase = str(ukr.get(step))
        return phrase
    if language == "rus":
        phrase = str(rus.get(step))
        return phrase
    if language == "eng":  
        phrase = str(eng.get(step))
        return phrase