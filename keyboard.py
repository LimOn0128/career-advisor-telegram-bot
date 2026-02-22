from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Начать тест'))
    markup.add(KeyboardButton('Категории профессий'))
    markup.add(KeyboardButton('Рекомендации по интересам'))
    markup.add(KeyboardButton('Мой профиль'))
    return markup

def categories_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('IT', callback_data='category_IT'),
               InlineKeyboardButton('Творчество', callback_data='category_Творчество'))
    markup.add(InlineKeyboardButton('Медицина', callback_data='category_Медицина'),
               InlineKeyboardButton('Бизнес', callback_data='category_Бизнес'))
    # Добавьте больше категорий
    markup.add(InlineKeyboardButton('Назад', callback_data='back_main'))
    return markup

def age_group_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Подросток (до 18)', callback_data='age_teen'),
               InlineKeyboardButton('Взрослый', callback_data='age_adult'))
    return markup
