import pyttsx3
import datetime
import speech_recognition as sr
from decouple import config

from random import choice
from utils import opening_text

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

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
    This function will great the user appropriately depending on the time of day.
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
        print("recognising...")
        query = r.recognize_google(audio, language='eng-us')
        if 'exit' not in query or 'stop' not in query:
            speak(choice(opening_text))
        else:
            hour = datetime.datetime.now().hour
            if hour >= 21 or hour < 4:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
    except Exception as e:
        speak("Sorry, I could not understand. Could you please say that again?")
        query = "None"
    return query


speak("initializing JARVIS...")
greet_user()
command = take_command()
