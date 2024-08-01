from flask import Flask, render_template, request,jsonify,session
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Configure Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_text_from_file(file_path):
    """Reads text from a file and returns it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return "File not found."
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return f"Error reading file: {e}"

def video_to_audio(video_path, audio_path):
    """Converts video file to audio file."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
        logging.info(f"Video to audio conversion successful: {video_path} to {audio_path}")
    except Exception as e:
        logging.error(f"Error processing video to audio: {e}")
        return f"Error processing video to audio: {e}"

def audio_to_text(audio_path):
    """Transcribes audio file to text."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        os.makedirs("result", exist_ok=True)  # Ensure the 'result' directory exists
        with open("result/transcribe.txt", "w", encoding='utf-8') as f:
            f.write(result["text"])
        logging.info(f"Audio to text transcription successful: {audio_path}")
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        return f"Error transcribing audio: {e}"

def generate_tags_chat(prompt_text):
    """Generates tags using Google Generative AI."""
    try:
        # Create a GenerativeModel instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt1="Generate SEO-optimized YouTube tags from the following text: ["+prompt_text+"] .Prioritize keywords with high search volume and low competition. Include variations and related terms. Return in plaintext format. "
        # Generate response using Gemini API
        response=model.generate_content(
            prompt1,
            generation_config=genai.GenerationConfig(
                max_output_tokens=100,
                temperature=0.5
            )
        )
        logging.info("Tag generation successful")
        # Return the generated text
        return response.text
    
    except Exception as e:
        logging.error(f"Error generating tags: {e}")
        return f"Error generating tags: {e}"
    
@app.route('/status')
def status():
    """Provides the current status of the file processing."""
    status = session.get('status', 'Processing not started')
    return jsonify({'status': status})

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    """Handles file upload and processing."""
    if 'file' not in request.files:
        return render_template('index.html', result='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', result='No selected file')

    max_file_size_mb = 100000
    
    if file.content_length > max_file_size_mb * 1024 * 1024:
        return render_template('index.html', result=f'File size exceeds {max_file_size_mb} MB limit')
    
    if file:
        video_path = "result/input.mp4"
        audio_path = "result/output.wav"

        try:
            os.makedirs("result", exist_ok=True)  
            file.save(video_path)
            logging.info(f"File uploaded: {file.filename}")

            session['status'] = 'Converting video to audio...'
            video_to_audio(video_path, audio_path)

            session['status'] = 'Converting audio to text...'
            audio_to_text(audio_path)

            session['status'] = 'Generating tags...'
            transcribed_text = read_text_from_file("result/transcribe.txt")
            tags_response = generate_tags_chat(transcribed_text)
            print(tags_response)
            response_message = tags_response

            with open("result/tags.txt", "w", encoding='utf-8') as f:
                f.write(response_message)

            logging.info("File processing completed successfully")
            session['status'] = 'File processing completed successfully'
            return render_template('index.html', result=response_message)
        except Exception as e:

            session['status'] = f"Error processing file: {e}"
            return render_template('index.html', result=f"Error processing file: {e}")

if __name__ == '__main__':
    app.run(debug=True)