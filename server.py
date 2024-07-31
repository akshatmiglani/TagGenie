from flask import Flask, render_template, request
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper
import os
from openai import OpenAI
from dotenv import load_dotenv
from celery import Celery
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except IOError as e:
        return f"Error reading file: {e}"

def video_to_audio(video_path, audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
    except Exception as e:
        return f"Error processing video to audio: {e}"

def audio_to_text(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        os.makedirs("result", exist_ok=True)  # Ensure the 'result' directory exists
        with open("result/transcribe.txt", "w", encoding='utf-8') as f:
            f.write(result["text"])
    except Exception as e:
        return f"Error transcribing audio: {e}"

def generate_tags_chat(prompt_text):

    try:
        # Create a GenerativeModel instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt1="Extract keywords from the following text: " + prompt_text
        # Generate response using Gemini API
        response=model.generate_content(
            prompt1,
            generation_config=genai.GenerationConfig(
                max_output_tokens=100,
                temperature=0.5
            )
        )
        print(response)
        # Return the generated text
        return response.text
    
    except Exception as e:
        return f"Error generating tags: {e}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', result='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', result='No selected file')

    max_file_size_mb = 25
    
    if file.content_length > max_file_size_mb * 1024 * 1024:
        return render_template('index.html', result=f'File size exceeds {max_file_size_mb} MB limit')
    
    if file:
        video_path = "result/input.mp4"
        audio_path = "result/output.wav"

        try:
            os.makedirs("result", exist_ok=True)  
            file.save(video_path)
            print("Converting audio to video")
            video_to_audio(video_path, audio_path)
            print("Converting audio to text")
            audio_to_text(audio_path)
            print("generating tags:")
            transcribed_text = read_text_from_file("result/transcribe.txt")
            tags_response = generate_tags_chat(transcribed_text)
            print(tags_response)
            response_message = tags_response

            with open("result/tags.txt", "w", encoding='utf-8') as f:
                f.write(response_message)
        
            return render_template('index.html', result=response_message)
        except Exception as e:
            return render_template('index.html', result=f"Error processing file: {e}")

if __name__ == '__main__':
    app.run(debug=True)
