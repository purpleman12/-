import os #Импортирование библиотеки ос
from google.cloud import dialogflow_v2beta1 as dialogflow#Импортирование библиотеки dialogflow_v2beta1 для работы с api dialogflow
import telebot #Импортирование библиотеки для работы с api бота телеграмм
from telebot import types#Импортирование библиотеки для работы с обьектами api бота
import random
# from model_fit import predict_function as pf
# from model_fit import tokenizer
# from model_fit import max_len
# from model_fit import model
# from model_fit import label_encoder
from model_fit1 import predict_cocktail as pc
from model_fit1 import model
from model_fit1 import cocktails

bot = telebot.TeleBot("6888259243:AAF_P5rFAcNqdtk74azzPezRfMI0das8q5k") #Api ключ бота

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D://Telegram_bot_ai/credentials2.0.json" #Настроенное окружение

project_id = "telegram-coctails-agent-h9ns"# Id проекта в google cloud


@bot.message_handler(commands=["start"])
def main(message):
    user = message.from_user
    bot.send_message(message.chat.id, f"Привет, {user.first_name}! Что вы хотите сделать?",reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(types.KeyboardButton("Информация по интерфейсу"),
                 types.KeyboardButton("Случайный"),
                 types.KeyboardButton("Анекдот"),
                 types.KeyboardButton("FAQ"))
    return keyboard




def detect_intent_text(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    print(f"Intent detected: {response.query_result.intent.display_name}")
    print(f"Confidence: {response.query_result.intent_detection_confidence}")
    print(f"Response: {response.query_result.fulfillment_text}")
    return ({response.query_result.fulfillment_text})

pref_message = ""

@bot.message_handler(func=lambda message: True) #принимает и отправляет сообщения польователю
def echo_all(message):
    # Получаем текст сообщения

    text_to_send = message.text
    session_id = "some_unique_id"

    user_id = message.from_user.id

    if (text_to_send == "FAQ"):
        bot.send_message(message.chat.id,"Вопрос: что такое Coctails_Ai_bot?\nОтвет: Coctails_Ai_bot — это чат-бот в мессенджере Telegram, который предоставляет рецепты коктейлей на основе ваших предпочтений и наличия ингредиентов.\nВопрос: как начать использовать Coctails_Ai_bot?\nОтвет: просто найдите бота в Telegram по имени @Coctails_Ai_bot и начните чат с ним. Бот подскажет вам инструкции по использованию.\nВопрос: Какие возможности предоставляет Coctails_Ai_bot?\nОтвет: Coctails_Ai_bot позволяет искать рецепты коктейлей по названию, типу напитка или ингредиентам, а также получать персонализированные рекомендации на основе ваших предпочтений.\nВопрос: как бот узнает мои предпочтения?\nОтвет: Вы можете сообщить боту о своих предпочтениях, выбрав соответствующие опции в меню или ответив на вопросы бота.\nВопрос: могу ли я добавить свои собственные рецепты в базу данных бота?\nОтвет: на данный момент бот не поддерживает добавление пользовательских рецептов, но мы работаем над этой функцией и надеемся внедрить ее в будущем.\nВопрос: могу ли я поделиться рецептом с друзьями?\nОтвет: да, бот предоставляет функцию для отправки рецепта в чат или поделиться им со своими контактами в Telegram.\nВопрос: как я могу предложить улучшения или сообщить о проблеме с ботом?\nОтвет: Вы можете отправить свои предложения или сообщить о проблеме, связанной с ботом, написав администратору бота через функцию обратной связи в меню.\n")
        return
    if (text_to_send == "Случайный"):
        bot.send_message(message.chat.id, detect_intent_text(project_id, "Случайный коктейль: " + session_id, cocktails[random.randint(1, 102)]))
        return
    #Общие запросы
    if(text_to_send!="FAQ" and text_to_send!="Случайный" and text_to_send!="Информация по интерфейсу" and text_to_send != "Анекдот"):
        # отправка сообщения в dialogflow
        dialogflow_response = detect_intent_text(project_id, session_id, text_to_send)
        dialogflow_message = dialogflow_response

        bot.send_message(user_id, dialogflow_message)

        pc_response = pc(model, text_to_send)
        print(pc_response)

        pc_dialogflow_response = detect_intent_text(project_id, session_id, pc_response)
        pc_dialogflow_message = pc_dialogflow_response
        bot.send_message(user_id, pc_dialogflow_message)
        pc_response = None
    if(text_to_send=="Информация по интерфейсу"):
        dialogflow_response = detect_intent_text(project_id, session_id, text_to_send)
        dialogflow_message = dialogflow_response

        bot.send_message(user_id, dialogflow_message)
        return
    if (text_to_send == "Анекдот"):
        dialogflow_response = detect_intent_text(project_id, session_id, text_to_send)
        dialogflow_message = dialogflow_response

        bot.send_message(user_id, dialogflow_message)
        return

if __name__ == '__main__':
    bot.polling(non_stop=True)