import telebot
from telebot.types import Message, CallbackQuery
import db
import keyboard
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, 'Привет! Я помогу выбрать карьеру. Выбери опцию:', reply_markup=keyboard.main_menu_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    if message.text == 'Начать тест':
        bot.send_message(message.chat.id, 'Сначала укажи свою возрастную группу:', reply_markup=keyboard.age_group_keyboard())
    elif message.text == 'Категории профессий':
        bot.send_message(message.chat.id, 'Выбери категорию:', reply_markup=keyboard.categories_keyboard())
    elif message.text == 'Рекомендации по интересам':
        bot.send_message(message.chat.id, 'Напиши свои интересы через запятую (e.g. IT, дизайн)')
    elif message.text == 'Мой профиль':
        user_data = db.get_user_data(message.from_user.id)
        if user_data:
            bot.send_message(message.chat.id, f'Возраст: {user_data[1]}\nИнтересы: {user_data[2]}\nТекущая работа: {user_data[3]}')
        else:
            bot.send_message(message.chat.id, 'Профиль пуст. Начни тест!')
    else:
        # Персонализированные рекомендации по тексту (интересам)
        interests = message.text
        professions = db.get_professions_by_interests(interests)
        if professions:
            for prof in professions:
                response = f'Профессия: {prof[1]}\nОписание: {prof[2]}\nНавыки: {prof[3]}\nОбразование: {prof[4]}\nЗарплата: {prof[5]}'
                bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, 'Ничего не нашел. Попробуй другие интересы!')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    if call.data.startswith('category_'):
        category = call.data.split('_')[1]
        professions = db.get_professions_by_category(category)
        if professions:
            for prof in professions:
                response = f'Профессия: {prof[1]}\nОписание: {prof[2]}\nНавыки: {prof[3]}\nОбразование: {prof[4]}\nЗарплата: {prof[5]}'
                bot.send_message(call.message.chat.id, response)
        else:
            bot.send_message(call.message.chat.id, 'Нет профессий в этой категории.')
    elif call.data.startswith('age_'):
        age_group = 'подросток' if call.data == 'age_teen' else 'взрослый'
        bot.send_message(call.message.chat.id, 'Теперь расскажи о своих интересах (через запятую):')
        bot.register_next_step_handler(call.message, save_interests, age_group)
    elif call.data == 'back_main':
        bot.send_message(call.message.chat.id, 'Главное меню:', reply_markup=keyboard.main_menu_keyboard())

def save_interests(message: Message, age_group):
    interests = message.text
    bot.send_message(message.chat.id, 'Текущая работа (если есть, иначе "нет"):')
    bot.register_next_step_handler(message, save_current_job, age_group, interests)

def save_current_job(message: Message, age_group, interests):
    current_job = message.text
    db.save_user_data(message.from_user.id, age_group, interests, current_job)
    # Здесь можно добавить логику рекомендаций на основе сохраненных данных
    professions = db.get_professions_by_interests(interests)
    if professions:
        bot.send_message(message.chat.id, 'Вот рекомендации:')
        for prof in professions:
            response = f'Профессия: {prof[1]}\nОписание: {prof[2]}'  # Упрощено для подростков
            bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, 'Рекомендаций пока нет.')

if __name__ == '__main__':
    # Загрузите начальные данные, если нужно
    # db.load_initial_data()
    bot.polling(none_stop=True)
