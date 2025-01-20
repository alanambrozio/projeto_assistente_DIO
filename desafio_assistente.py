import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import pyjokes
import wikipedia
import webbrowser
import tempfile
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(f"You said: {said}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that. Please try again.")
        except sr.RequestError:
            speak("Sorry, the speech recognition service is currently unavailable.")
    return said

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.close()
        tts.save(temp_audio.name)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio.name)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 

    pygame.mixer.music.stop()

    pygame.mixer.quit()  

    os.remove(temp_audio.name)

if __name__ == "__main__":
    while True:
        print("I am listening...")
        text = get_audio().lower()
        if 'youtube' in text:
            speak("Opening YouTube")
            url = "https://www.youtube.com"
            try:
                webbrowser.open(url)
            except webbrowser.Error:
                speak("I couldn't open YouTube. Please check your internet connection.")
        elif 'camp' in text:
            speak("Opening bootcamp")
            url = "https://www.dio.me"
            try:
                webbrowser.open(url)
            except webbrowser.Error:
                speak("I couldn't open DIO. Please check your internet connection.")
        elif 'search' in text:
            speak('Searching Wikipedia...')
            query = text.replace('search', "").strip()
            if not query:
                speak("You didn't specify what to search for. Please try again.")
                continue
            try:
                result = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(result)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("Your search term is ambiguous. Try being more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find anything on Wikipedia with that query.")
        elif 'joke' in text:
            speak(pyjokes.get_joke())
        elif 'exit' in text:
            speak('Goodbye, till next time.')
            if pygame.mixer.get_init():
                pygame.mixer.quit()
            exit()
