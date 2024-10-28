import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recogniser=sr.Recognizer()
engine = pyttsx3.init()
newsapi="6a6619cb0bf64bc0b6d6e89b3fd68a41"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 



def aiProcess(command):
    client = OpenAI(api_key="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",
)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named alexa skilled in general tasks like Alexa and Google Cloud . give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    print(completion.choices[0].message.content)



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif"open youtube"in c.lower():
        webbrowser.open("https://youtube.com")
    elif"open linkedin"in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=music_library.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r= requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            data =r.json()
            articles=data.get('articles',[])

            for article in articles:
                speak(article['title'])
    
    else:
        output=aiProcess(c)
        speak(output)
        pass

if __name__=="__main__":  
    speak("initializing Alexa")

    while True:

        # listen for the word alexa
        # obtain audio from the microphone

        r=sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as  source:
                print("listening...")
                audio=r.listen(source,timeout=2,phrase_time_limit=1)
            

            word=r.recognize_google(audio)
            if(word.lower()=="alexa"):
                speak("yes")
                # listen for command
                with sr.Microphone() as  source:
                    print("alexa active...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command) 

        except Exception as e:
            print(" error;{0}".format(e))

