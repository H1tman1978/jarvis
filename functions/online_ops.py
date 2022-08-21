import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config


EMAIL = config("EMAIL")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
NEWS_API_KEY = config("NEWS_API_KEY")
WEATHER_ID = config("OPENWEATHER_API_KEY")
TMDB_API_KEY = config("TMDB_API_KEY")


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    return wikipedia.summary(query, sentences=2)


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp-mail.outlook.com", 587)
        s.starttls()
        s.login(EMAIL, EMAIL_PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    headlines = []
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}&category=general").json()
    articles = response["articles"]
    for article in articles:
        headlines.append(article["title"])
    return headlines[:5]


def get_weather_report(city):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_ID}&units=imperial").json()
    weather = response["weather"][0]["main"]
    temperature = response["main"]["temp"]
    feels_like = response["main"]["feels_like"]
    high = response["main"]["temp_max"]
    low = response["main"]["temp_min"]
    humidity = response["main"]["humidity"]
    wind_speed = response["wind"]["speed"]
    wind_direction = response["wind"]["deg"]
    return weather, f"{temperature}\u00B0 F", f"{feels_like}\u00B0 F", f"{high}\u00B0 F", f"{low}\u00B0 F", f"{humidity}%", f"{wind_speed} mph", f"{wind_direction}\u00B0"


def get_trending_movies():
    trending_movies = []
    response = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = response["results"]
    for result in results:
        trending_movies.append(result["original_title"])
    return trending_movies[:5]
