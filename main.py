from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import psycopg2
import os
from dotenv import load_dotenv

# Загрузите переменные из .env
load_dotenv()

# Получите токен из переменной окружения
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден в .env файле или переменных окружения!")

# Остальной код бота (как в предыдущем примере)
# ...

# Получите параметры из .env
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432")  # Значение по умолчанию
}

# Проверка: все ли переменные загружены
if not all(DB_CONFIG.values()):
    raise ValueError("Не все переменные окружения для БД установлены!")

# Функция для подключения к БД
def connect_db():
    print("🔌 Подключение к БД...")
    try:
        print("🔌 Подключение к БД с параметрами:", DB_CONFIG)
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Успешное подключение к БД")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return None

# Обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет! Я сохраню все твои сообщения в базу данных.")

# Обработчик текстовых сообщений
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Успешное подключение к БД")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")  # Покажет точную ошибку
        return None

def save_message(update, context):
    username = update.message.from_user.username
    message = update.message.text
    print(f"📩 Получено сообщение: {username} -> {message}")

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            print(f"Выполняю запрос: INSERT INTO public.messages (username, message) VALUES ('{username}', '{message}');")
            cur.execute(
                "INSERT INTO public.messages (username, message) VALUES (%s, %s);",
                (username, message)
            )
            conn.commit()
        except Exception as e:
            print(f"❌ Ошибка записи в БД: {e}")  # Покажет точную ошибку
        finally:
            conn.close()

    # Ответ пользователю
    update.message.reply_text(f"Сообщение сохранено: {message}")

# Основная функция
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, save_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
