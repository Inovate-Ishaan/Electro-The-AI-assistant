import sounddevice as sd
import speech_recognition as sr
import numpy as np
import os
from scipy.io.wavfile import write
from google import genai
import pyttsx3 as pytts
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import soundfile as sf
import logging
import random
from main_scripts import music_downloader_yt
import time
import serial
import subprocess


try:
    port_name = "/dev/ttyACM0"  # CHANGE ACCORDINGLY
    ser = serial.Serial(port_name, 115200)   # communication with arduino
    print("connected to arduino")

except:
    print("failed to communicate with arduino")



#logging code
logging.basicConfig(
    filename="program-log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%d-%m-%Y %H:%M",
)

api_key_gemini = 'AIzaSyB0w4wSoHH7EsGVu6Hk4mn6t19SNTGxtfQ'
api_key_gemini_2 = 'AIzaSyB1wyyEtAnWzmuTX57dFUtTRDtvlemH2Cs'
client = genai.Client(api_key = api_key_gemini_2)
elevenlabs = ElevenLabs(api_key="sk_5e10860ba7729998c76a43a73cb6e16315be894c29623645")


base_prompt = """You are a table-top AI assistant. The following text is the user's query.

If the user asks or intends to play music, respond ONLY with:
play_music <song name>

If the user asks or intends to turn on rainbow lights, respond ONLY with:
rainbow_lights


For all other queries, give a short, precise, concise response without special characters. Begin with a brief introductory line. If the user asks for an explanation, then elaborate the response.
\n"""

r = sr.Recognizer()




def play_tones(filename):
    try:
        print("Inside try")

        data, fs = sf.read(filename)
        sd.play(data, fs)
        sd.wait()
    except FileNotFoundError:
        print("Inside except 1")
        logging.warning(f"error in play_tones \ntone file {filename} not found")
    except Exception as e:
        print("Inside except 2")
        logging.warning(f"error in play_tones \n {e}")


stt_success = False

def stt():
    """This function should be triggerd after wake word had been detected. It uses sr library to record audio, google api
    for stt, then saves a .wav file using scipy -- but use of saving has not been found yet"""
    try:
        with sr.Microphone() as source:
            print("Speak Now")
            audio = r.listen(source)              #gives an AudioData object

        data = np.frombuffer(audio.get_raw_data(), np.int16)     #convert AudioData to Numpy array
        fs = audio.sample_rate
        write('output.wav', fs, data)
        text = r.recognize_google(audio)
        print(text)
        full_prompt = base_prompt + text
        global stt_success
        stt_success= True
        print("STT passed")
        return full_prompt
    
    except:
        print("STT failed")
        fallback_responses = ["Sorry... I didn't get that", "Had some trouble listening, could you please repeat that?","Show some energy man, speak loud and clear..."]
        rp = random.choice(fallback_responses)
        return rp



def fetch_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def process_response(response):
    if "play_music" in response:
        print(response)
        query = response[10:]
        music_handler_response = music_downloader_yt.get_music(query)
        if music_handler_response[0] is True:
            try:
                music_file = subprocess.Popen(["python3", "/project_electro/Electro---The-AI-assistant/main_scripts/music_file.py"])
            except:
                print("error opening the music_file")



                ###### need to add code for music fft....

            title = music_handler_response[1]
            play_response(f"Playing {title} from YouTube...")
            music_path = "/project_electro/Electro---The-AI-assistant/Precise-Engine/music.wav"
            play_tones(music_path)
            os.remove(music_path)
            return f"Played {title}"
        else:
            return f"Unable to play {query}. Some error occurred..."
        
    if "rainbow_lights" in response:
        send_arduino(5) # command for rainbow lights


    else:
        return response


def play_response(ai_response):
    print(f"AI Response: {ai_response}")

    #play using ElevenLabs
    try:
        audio = elevenlabs.text_to_speech.convert(
            text = ai_response,
            voice_id="weA4Q36twV5kwSaTEL0Q",
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
        )
        #monika id sunJnCSgZmOuefCgCWBd
        #defualt voice id: JBFqnCBsd6RMkjVDRZzb
        print("fine till here")
        play(audio)

    #using pyttsx3
    
    except:
        logging.warning("Couldn't reach Elevenlabs, Played using google TTS")
        tts_engine = pytts.init()
        #switch to female voice
        voices = tts_engine.getProperty("voices")
        tts_engine.setProperty('rate', 125)
        tts_engine.setProperty('voice', voices[0].id)
        tts_engine.say(ai_response)
        tts_engine.runAndWait()
        return
    
    

def main():
    print("Wake word detected!")
    #filename = f"audio_{datetime.now().strftime('%H%M%S')}.wav"
    #record_audio(filename)

    #play hearing tone
    play_tones("//project_electro/Electro---The-AI-assistant/sfx/google.mp3")
    print("Listening...")

    #speech to text 
    prompt = stt()
    if stt_success:
        #play confirmaton tone
        play_tones("/project_electro/Electro---The-AI-assistant/sfx/meet.mp3")

        ai_response = fetch_response(prompt)
        processed_response = process_response(ai_response)
        play_response(processed_response)

    else:
        play_tones("/project_electro/Electro---The-AI-assistant/sfx/listening.wav")
        play_response(prompt)
        
    #print("Say Electro!!!")

def send_arduino(command):
    ser.write(bytes([command])) # here used [] to send the exact value as a byte otherwise it sends command for making an array of bytes of size 1 that has value 0 [0...0] instead of [0.....01]





if __name__ == "__main__":
    main()






