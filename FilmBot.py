import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator
import requests

# Ваш токен для Telegram бота
TOKEN = '7098666675:AAGCalQAW8r79aWnryTZR1uHe_3wrgTrXnM'
# Ваш ключ API для OMDb
OMDB_API_KEY = '2e609034'

def start(update, context):
    update.message.reply_text('Привет! Я бот для поиска фильмов по названию. Просто отправь мне название фильма.')

def search_movie(update, context):
    movie_title = update.message.text

    if not movie_title:
        update.message.reply_text('Пожалуйста, укажите название фильма для поиска.')
        return

    # Переводим введенное пользователем название на английский язык
    translator = Translator()
    translated_title = translator.translate(movie_title, dest='en').text

    response = requests.get(f'http://www.omdbapi.com/?t={translated_title}&apikey={OMDB_API_KEY}&plot=full')

    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            title = data['Title']
            year = data['Year']
            genre = data['Genre']
            imdb_rating = data['imdbRating']
            plot = data['Plot']
            imdb_link = f"https://www.imdb.com/title/{data['imdbID']}/"

            # Переводим описание на русский язык с помощью googletrans
            translated_plot = translator.translate(plot, dest='ru').text

            message = f"Название: {title}\nГод выпуска: {year}\nЖанр: {genre}\nРейтинг: {imdb_rating}\nОписание: {translated_plot}\nСсылка на IMDb: {imdb_link}"
            update.message.reply_text(message)
        else:
            update.message.reply_text("Фильм не найден.")
    else:
        update.message.reply_text(f"Ошибка запроса к OMDb API: {response.status_code}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search_movie))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_movie))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
