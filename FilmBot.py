import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

TOKEN = '7098666675:AAGCalQAW8r79aWnryTZR1uHe_3wrgTrXnM'


def start(update, context):
    update.message.reply_text('Привет! Я бот для поиска фильмов по названию. Просто отправь мне название фильма.')


def search_movie(update, context):
    movie_title = update.message.text

    if not movie_title:
        update.message.reply_text('Пожалуйста, укажите название фильма для поиска.')
        return

    response = requests.get(f'http://www.omdbapi.com/?t={movie_title}&apikey=2e609034&plot=full')
    data = response.json()

    if data['Response'] == 'True':
        title = data['Title']
        year = data['Year']
        genre = data['Genre']
        imdb_rating = data['imdbRating']
        plot = data['Plot']
        imdb_link = f"https://www.imdb.com/title/{data['imdbID']}/"

        message = f"Название: {title}\nГод выпуска: {year}\nЖанр: {genre}\nРейтинг: {imdb_rating}\nОписание: {plot}\nСсылка на IMDb: {imdb_link}"
    else:
        message = "Фильм не найден."

    update.message.reply_text(message)


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
