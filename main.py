import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary   # make sure this file exists
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]  # everything after 'play'
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak("Sorry, I don't know that song.")
        except Exception:
            speak("Please say the song name properly.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            # --- Listen for wake word ---
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=1)  # NEW
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)

            word = recognizer.recognize_google(audio)
            print("You said:", word)

            if "jarvis" in word.lower():
                speak("Yes, how can I help?")
                time.sleep(1)

                # --- Listen for command ---
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)  # NEW
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)

                try:
                    command = recognizer.recognize_google(audio)
                    print("Heard command:", command)  # DEBUG print
                    processCommand(command)
                    time.sleep(2)
                except sr.UnknownValueError:
                    print("Could not understand the command.")
                    speak("Sorry, I didn't catch that. Please repeat.")
        
        except sr.WaitTimeoutError:
            print("No speech detected. Trying again...")
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except Exception as e:
            print("Error:", e)
