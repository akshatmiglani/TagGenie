from flask import Flask,render_template,request
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def video_to_audio(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)



def audio_to_text(audio_path):
    model = whisper.load_model("base")
    result=model.transcribe(audio_path)

    with open("result/transcribe.txt","w") as f:
        f.write(result["text"])

def generate_tags_chat(prompt_text):
    response =client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will be provided with a block of text, and your task is to extract a list of keywords from it which I can use as Tags for my Youtube Video."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.5,
        max_tokens=64,
        top_p=1
    )
    return response


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

        file.save(video_path)

        video_to_audio(video_path,audio_path)
        audio_to_text(audio_path)

        transcribed_text = read_text_from_file("result/transcribe.txt")
        tags_response = generate_tags_chat(transcribed_text)

        response_message = tags_response.choices[0].message.content

        with open("result/tags.txt", "w") as f:
            f.write(response_message)

        
        return render_template('index.html', result=response_message)


if __name__ == '__main__':
    app.run(debug=True)