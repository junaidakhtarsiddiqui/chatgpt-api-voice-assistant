import gradio as gr
import openai
import pyttsx3

openai.api_key = "Your_API_Key_Here"

messages = [
    {"role": "system", "content": "You are a Therapist."}
    # {"role": "user", "content": transcript["text"]}
    # # {"role": "assistant", "content": system_message},
    # # {"role": "user", "content": "Where was it played?"}
]

def transcribe(Audio):
    global messages
    print(Audio)

    audio_file= open(Audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    system_message= response["choices"][0]["message"]["content"]
    
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Speak the system message
    engine.say(system_message)
    engine.runAndWait()

    messages.append({"role": "assistant", "content": system_message})

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"


    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()


ui.launch(share=True)
