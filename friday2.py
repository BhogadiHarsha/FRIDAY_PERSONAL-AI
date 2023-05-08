#IMPORTING NECESSARY LIBRARIES
import openai
import pyttsx3
import speech_recognition as sr
import time

#OPENAI KEY
openai.api_key = "(creat and add your open ai key)"

#INTIALIZING TEXT TO SPEECH ENGINE
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#FUNCTION TO TRANSCRIBE AUDIO TO TEXT
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    
    # Open audio file and record audio
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        # Transcribe audio using Google Speech Recognition API
        return recognizer.recognize_google(audio)
    except:
        print('sorry i didnt understand')

#FUNCTION TO GENERATE FRIDAY RESPONSE USING OPENAI API
def generate_response(prompt):
    if "what is your name" in prompt.lower():
        return "Hello there! I am Friday, an intelligent assistant here to help you maximize your productivity and simplify your workload. With my advanced capabilities and vast knowledge, I can assist you with various tasks and provide valuable insights to streamline your work processes. From scheduling appointments to conducting research, I am always available to make your life easier. Let's work together and achieve your goals more efficiently!"
    if "who created you"in prompt.lower():
        return  "I am an advanced system that was created by a team of ingenious individuals from GRIET college: Harsha, Nithin, and Vaibhav. These three visionary individuals have harnessed their intelligence, creativity, and technological expertise to design and build me from the ground up."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response["choices"][0]["text"]

#FUNCTION TO SPEAKTEXT USING TEXT TO SPEECH ENGINE
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
#MAIN FUNCTION TO RECORD AND PROCESS USER INPUT
def main():
    filename = "output.wav"
    while True:
        #say friday to record
        print("say 'friday' to start recording your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer() 
            audio = recognizer.listen(source)
            try:#check audio if user said friday
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "friday":
                    print("say your question")
                    #friday starts recording user question
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said: {text}")
                        response = generate_response(text)
                        print(f"Friday says: {response}")
                        speak_text(response)
            except Exception as e:
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()
