from random import choice

import requests

from utils import opening_text
from pprint import pprint

import pyttsx3
import datetime
import speech_recognition as sr
from decouple import config

from functions.os_ops import open_camera, open_pycharm, open_discord, open_calculator, open_steam, open_cmd
from functions.online_ops import find_my_ip, search_on_wikipedia, play_on_youtube, search_on_google, send_email, \
    get_latest_news, get_weather_report, get_trending_movies, get_trending_tv_shows, get_random_joke, \
    send_whatsapp_message, get_random_advice

USERNAME = config('USER')
BOTNAME = config('BOTNAME')
SUSANAS_PHONE_NUMBER = config('SUSANAS_PHONE_NUMBER')

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    """
    This function implements text-to-speach.
    :param audio: A string that you want converted to audio.
    :return:
    """
    engine.say(audio)
    engine.runAndWait()


def greet_user():
    """
    Greets the user appropriately depending on the time of day.
    :return:
    """
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning sir.")
    elif 12 <= hour < 16:
        speak("Good afternoon sir.")
    else:
        speak("Good evening sir.")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("recognizing...")
        query = r.recognize_google(audio, language='eng-us')
    except Exception as e:
        print(e)
        query = "None"
    return query


if __name__ == '__main__':
    speak("initializing JARVIS...")
    greet_user()
    while True:
        command = take_command().lower()
        match command.split():
            case ["open", obj]:
                match obj:
                    case "camera":
                        speak(choice(opening_text))
                        open_camera()
                    case "pycharm":
                        speak(choice(opening_text))
                        open_pycharm()
                    case "discord":
                        speak(choice(opening_text))
                        open_discord()
                    case "steam":
                        speak(choice(opening_text))
                        open_steam()
                    case "command":
                        speak(choice(opening_text))
                        open_cmd()
                    case "calculator":
                        speak(choice(opening_text))
                        open_calculator()
                    case _:
                        speak("I'm sorry, but that feature hasn't been implemented...yet.")
            case ["ip", "address"]:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')
            case ["send", method]:
                match method:
                    case "email":
                        speak("On what email address do I send sir? Please enter in the console: ")
                        receiver_address = input("Enter email address: ")
                        speak("What should be the subject sir?")
                        subject = take_command().title()
                        speak("What is the message sir?")
                        message = take_command()
                        if send_email(receiver_address, subject, message):
                            speak("I've sent the email sir.")
                        else:
                            speak("Something went wrong while I was sending the mail. Please check the error logs sir.")
                    case "whatsapp":
                        speak('On what number should I send the message sir? Please enter in the console: ')
                        number = input("Enter the number: ")
                        speak("What is the message sir?")
                        message = take_command().lower()
                        send_whatsapp_message(number, message)
                        speak("I've sent the message sir.")
                    case "susana":
                        speak("What message do you want to send to Susana?")
                        message = take_command().lower()
                        send_whatsapp_message(SUSANAS_PHONE_NUMBER, message)
                        speak("Message sent to Susana, sir.")
            case ["joke"]:
                speak(f"Hope you like this one sir")
                joke = get_random_joke()
                speak(joke)
                speak("For your convenience, I am printing it on the screen sir.")
                pprint(joke)
            case ["advice"]:
                speak("Here's some advice for you, sir.")
                advice = get_random_advice()
                speak(advice)
                speak("For your convenience, I am printing it on the screen sir.")
                pprint(advice)
            case ["search", site]:
                match site:
                    case "google":
                        speak('What do you want to search on Google, sir?')
                        query = take_command().lower()
                        search_on_google(query)
                    case "wikipedia":
                        speak('What do you want to search on Wikipedia, sir?')
                        search_query = take_command().lower()
                        results = search_on_wikipedia(search_query)
                        speak(f"According to Wikipedia, {results}")
                        speak("For your convenience, I am printing it on the screen sir.")
                        print(results)
            case ["trending", option]:
                match option:
                    case "movies":
                        speak(f"Some of the trending movies are: {get_trending_movies()}")
                        speak("For your convenience, I am printing it on the screen sir.")
                        print(*get_trending_movies(), sep='\n')
                    case "tv":
                        speak(f"Some of the trending tv shows are: {get_trending_tv_shows()}")
                        speak("For your convenience, I am printing it on the screen sir.")
                        print(*get_trending_tv_shows(), sep='\n')
            case ["news"]:
                speak(f"I'm reading out the latest news headlines, sir")
                speak(get_latest_news())
                speak("For your convenience, I am printing it on the screen sir.")
                print(*get_latest_news(), sep='\n')
            case ["watch", "youtube", "video", "on", subject]:
                speak(f"Playing a YouTube video on {subject}, sir. ")
                play_on_youtube(subject)
            case ["youtube"]:
                speak('What do you want to play on Youtube, sir?')
                video = take_command().lower()
                play_on_youtube(video)
            case ["weather", "in", city]:
                speak(f"Getting current weather for {city}...")
                weather, temperature, feels_like, high, low, humidity, wind_speed, wind_direction = get_weather_report(city)
                speak(f"Currently, {city} has {weather}.")
                speak(f"The current temperature is {temperature}, but it feels like {feels_like}.")
                speak(f"The high will be {high} with a low of {low}.")
                speak(f"Humidity is currently {humidity}.")
                speak(f"Winds are {wind_speed} at {wind_direction}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Weather in {city}: {weather}\n"
                      f"Temperature: {temperature}\n"
                      f"Feels like: {feels_like}\n"
                      f"High: {high}\n"
                      f"Low: {low}\n"
                      f"Humidity: {humidity}\n"
                      f"Wind Speed: {wind_speed}\n"
                      f"Wind Direction: {wind_direction}")
            case ["weather"]:
                ip_address = find_my_ip()
                city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                speak("Getting your local weather...")
                weather, temperature, feels_like, high, low, humidity, wind_speed, wind_direction = get_weather_report(city)
                speak(f"Currently, {city} has {weather}.")
                speak(f"The current temperature is {temperature}, but it feels like {feels_like}.")
                speak(f"The high will be {high} with a low of {low}.")
                speak(f"Humidity is currently {humidity}.")
                speak(f"Winds are {wind_speed} at {wind_direction}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Weather in {city}: {weather}\n"
                      f"Temperature: {temperature}\n"
                      f"Feels like: {feels_like}\n"
                      f"High: {high}\n"
                      f"Low: {low}\n"
                      f"Humidity: {humidity}\n"
                      f"Wind Speed: {wind_speed}\n"
                      f"Wind Direction: {wind_direction}")
            case ["exit"] | ["quit"]:
                hour = datetime.datetime.now().hour
                if hour >= 21 or hour < 4:
                    speak("Good night sir, take care!")
                else:
                    speak("Have a good day sir!")
                break
