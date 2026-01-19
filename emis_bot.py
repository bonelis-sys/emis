import telebot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Токен бота от @BotFather
BOT_TOKEN = '8572927019:AAH3iLGpjlecdTO2Bkqr25ey7JhUu-Hl0Vw'
bot = telebot.TeleBot(BOT_TOKEN)

# SMTP настройки (пример для Gmail: включи 2FA и App Password)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'  # Твой email
SMTP_PASS = 'your_app_password'     # App Password, не основной пароль
TARGET_EMAIL = 'emis_ro@mail.ru'

user_states = {}  # Словарь для состояний пользователей

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ваш вопрос по еМИС?")
    bot.register_next_step_handler(message, process_question)

def process_question(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Нет username"
    
    # Формируем email
    subject = f"Вопрос по еМИС от Telegram пользователя {user_id}"
    body = f"Вопрос: {message.text}\n\nПользователь ID: {user_id}\nUsername: @{username}\nChat ID: {message.chat.id}"
    
    # Отправка email
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = TARGET_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        bot.send_message(message.chat.id, "Спасибо! Ваш вопрос отправлен на emis_ro@mail.ru.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка отправки: {str(e)}")
    
    # Сброс состояния
    if user_id in user_states:
        del user_states[user_id]

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Получил: {message.text}")

print("Тест: отправь боту любое сообщение")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
