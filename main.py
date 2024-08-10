from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from openai import OpenAI

import utils

load_dotenv()

class Assistant:
    def __init__(self, language='en'):
        self.language = language.lower().strip()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.openai_client = OpenAI()
        self.messages = []
        self.messages.append({ "role": "system", "content": utils.read_file('promting.txt') })
        self.output_file = "assets/response.mp3"  # File to save the generated speech

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def say(self, text):
        if text:
            tts = gTTS(text=text, lang=self.language)
            tts.save(self.output_file)
            playsound(self.output_file, block=True)

    def get_response(self, text):
        if text:
            self.messages.append({ "role": "user", "content": text })
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages
            )
            return response.choices[0].message.content
        return "Sorry, I didn't catch that."

def main():
    assistant = Assistant(language='ar')
    
    print("Hello! I am your voice assistant. Speak to me.")
    
    while True:
        text = assistant.listen()
        if text:
            response = assistant.get_response(text)
            info = utils.extract_cmd_info(response)
            
            if info == None:
                print(f"Response: {response}")
                assistant.say(response.replace('[GEN]', ''))
            else:
                if info.get('cmd') == 'YouTube':
                    assistant.say("حاضر")
                    utils.play_song(info.get('song_name'))

                if info.get('cmd') == 'Time':
                    assistant.say(utils.get_current_time())

if __name__ == '__main__':
    main()
