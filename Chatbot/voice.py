import speech_recognition as sr
import pyttsx3

def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine

def speak(engine, command):
    engine.say(command)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio).lower()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that. Please try again.")
    return ""
