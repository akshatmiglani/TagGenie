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
    
        # Create the model
        generation_config = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction="You are an experienced SEO expert. Your task is to generate keywords from transcriptions focusing on high search volume and low competition. You should always return 50-70 keywords separated by comma only, no trailing or succeding text.",
        )

        chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                "hey expert, generate tags for : \" Hello, we have created a secure file distributed system for examination purpose. We have been told that we have to create three rules for that admin examiner at each data. We have prepared different functionality for different rules. Let me talk about admin. First of all, whether going to admin, we have created a good login system using GWP tokens and having a good authentication system so that each user can use their own functionality. No one can use any other functionality as possible. For admin functionality, we have created that admin can only create the initials of examiner as an administrator. No one else can create that. Admin can view all the papers and the different versions. Admin can upload or update the different papers and other versions. And admin, the main feature is admin can access all the logs on the real time, which the user has logged in or signed in at which time and at which time stamp admin has all the access of our data. The second rule is for examiner. In most of the cases, examiner will be able to upload and update which other files you want to share. Suppose we have three examiners, one, two and three. So examiner one will be able to view the files which she has himself uploaded or herself uploaded here and same for examiner two and three. And the invigilator will be able to view the paper according to the schedule time. And if you will also get a notification when the schedule will be happening of the new paper is going to be scheduled. Now let's move to the hands-on of this all we have. First of all, we will see how admin works. First of all, it will go to the admin panel and we will get the features. We will set this at the role and we will be controlling. We have the admin panel. Here is add user functionality where admin can add any user they want. For example, I am adding any random users here and user. Then as user has been added successfully. Then you can see the real time logs that this user has been added with the timestamp so that it can get all the things and who has logged in at which time. And in the future we can add the data analysis functionality also in this log content. So to get the malicious activity if happened in our bagad. Then we have a function to upload a paper. For example, I upload a paper named XYZ and to get support at this time and any time if possible. So I post at the 17 and I choose a random file for an example and I upload here. Then you can see the paper has been uploaded successfully and here it can view all the papers with its version and you can see the new paper also it has been uploaded here. This is all the functionality that we have given to admin. Now we will see how the examiner functionality works. For example, I log into examiner and then we change the role and log into examiner. Here also we have given the upload a paper functionality so that examiner obviously is the paper. Then we have updated the file. We can update the file and we can get through its new version if possible. And then we can view all and download each and every paper here. We can see the indicator in how the installation functionality works. We will move to the indicator. Immigilator can only see or view the document or the file that we have created. With a watermark also, we have a watermark functionality. Through this we can get through the name authentication and the indicator can see all the different papers which are latest paper which are uploaded. Here is a term latest paper which are uploaded with all the watermarks. Now we will get through the authentication papers. For example, if someone tries to log in change the demo on have a cross side 4G or a URL 4GD, he cannot because we have a good authentication system. Apart from this if someone tries to log in with different role, for example, I mean he will be denied the log in for the backend of this data model. So now I will be explaining the backend. First we have to I will be telling about the data modeling that we have done. For the log stable, he will have the action username and time stamp. It is the basic schema. Then for the users, we will have the default ID by which is set by a MongoDB and we will have a password in a hash format. It is done by the click library and the respective role for the user. Then for the paper schema, we have like the default ID which is the file MongoDB. Then we have the title for the document. Then we have the versions version ID and it says 3 key. We also have the schedule time for when the file will be need to be viewed by the which later. Then we have uploaded by which is referring to the user which has uploaded examiner which has uploaded this file and we have the created and updated time in this schema. So this is also all about the data with modeling. Now I will be telling about how our backend works. So we have implemented S3 functionality for the storage. So first we have the examiner will upload the file. So we will do some image processing and we will be adding the bottom up using image bottom up library and after that we will store that document in S3 bucket. I will show you a demo of that as well. So this is our S3 bucket which is secure exam paper. So here all the files will be available since it is provided by AWS Cloud and we have control over the ACLs. There is a lot of security here and it has less chances of being attacked by some malicious person. So we have all the files which are available. So as we can see we just found the last appropriate files as well. So our main storage is S3 and apart from this two folders client and server. First we have all the server we have realized to react and tailwind for this. In the source folder we have components and admin examiner, emigrator etc. The different dashboard that we have shown you. We have the app.js which has the routes for everything and we also like mentioned we have protected it so that no one can without the role no one can access this. We have the server file in which we have middleware for authentication which is the tokens so that we can find out which user has uploaded what file. Then we have the models where we have defined the schema. Here is a log, paper schema and user schema. Then we have different routes. So all the long you will be done by this API. We have paper routes which will be having multiple APIs that we showed you earlier. So here is implementation of all the APIs which we can go through our code base for this. Then we have user routes. So we are same. This thing goes for this. Then we have the main index file and this will be the temporary storage which will be clean automatically in one hour of the server.\"",
            ],
            },
            {
            "role": "model",
            "parts": [
                "secure file distributed system, examination system, secure file storage, exam paper storage, admin panel, examiner panel, invigilator panel, user authentication, GWP tokens, authentication system, role-based access control, user management, add user functionality, real-time logs, data analysis, malicious activity detection, paper upload, paper update, paper versioning, file upload, file update, file download, watermark functionality, cross-site scripting prevention, URL forgery prevention, data modeling, MongoDB, schema design, log schema, user schema, paper schema, S3 storage, AWS Cloud, ACLs, security, image processing, image watermarking, React, Tailwind CSS, dashboard, routes, authentication middleware, API, paper routes, user routes, temporary storage, backend development, data security, exam security, online examination, secure exam platform, exam management system, exam paper management, exam paper distribution, exam paper access control, exam paper tracking, exam paper analytics, exam paper security, exam paper integrity, exam paper plagiarism detection, exam paper watermarking, exam paper version control, exam paper scheduling, exam paper notification, exam paper download, exam paper viewing, exam paper upload, exam paper update, exam paper storage, exam paper retrieval, exam paper management system, exam paper administration, exam paper security system, exam paper distribution system, exam paper access control system, exam paper tracking system, exam paper analytics system, exam paper plagiarism detection system, exam paper watermarking system, exam paper version control system, exam paper scheduling system, exam paper notification system, exam paper download system, exam paper viewing system, exam paper upload system, exam paper update system, exam paper storage system, exam paper retrieval system, exam paper management software, exam paper administration software, exam paper security software, exam paper distribution software, exam paper access control software, exam paper tracking software, exam paper analytics software, exam paper plagiarism detection software, exam paper watermarking software, exam paper version control software, exam paper scheduling software, exam paper notification software, exam paper download software, exam paper viewing software, exam paper upload software, exam paper update software, exam paper storage software, exam paper retrieval software, online exam platform, online exam system, online exam software, online exam management, online exam security, online exam administration, online exam proctoring, online exam assessment, online exam evaluation, online exam grading, online exam feedback, online exam analytics, online exam reporting, online exam results, online exam platform development, online exam system development, online exam software development, online exam management development, online exam security development, online exam administration development, online exam proctoring development, online exam assessment development, online exam evaluation development, online exam grading development, online exam feedback development, online exam analytics development, online exam reporting development, online exam results development, secure file storage system, secure file sharing system, secure file distribution system, secure file access control system, secure file management system, secure file storage solution, secure file sharing solution, secure file distribution solution, secure file access control solution, secure file management solution, secure file storage service, secure file sharing service, secure file distribution service, secure file access control service, secure file management service, secure file storage platform, secure file sharing platform, secure file distribution platform, secure file access control platform, secure file management platform, secure file storage technology, secure file sharing technology, secure file distribution technology, secure file access control technology, secure file management technology, secure file storage solution, secure file sharing solution, secure file distribution solution, secure file access control solution, secure file management solution, secure file storage service, secure file sharing service, secure file distribution service, secure file access control service, secure file management service, secure file storage platform, secure file sharing platform, secure file distribution platform, secure file access control platform, secure file management platform, secure file storage technology, secure file sharing technology, secure file distribution technology, secure file access control technology, secure file management technology. \n",
            ],
            },
        ]
        )

        response = chat_session.send_message("Generate tags for: '"+prompt_text+"'")
        logging.info("Tag generation successful")
        # Return the generated text
        return response.text

    except Exception as e:
        logging.error(f"Error generating tags: {e}")
        return f"Error generating tags: {e}"
    
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

            
            video_to_audio(video_path, audio_path)

            
            audio_to_text(audio_path)

            
            transcribed_text = read_text_from_file("result/transcribe.txt")
            tags_response = generate_tags_chat(transcribed_text)
            print(tags_response)
            response_message = tags_response

            with open("result/tags.txt", "w", encoding='utf-8') as f:
                f.write(response_message)

            logging.info("File processing completed successfully")
           
            return render_template('index.html', result=response_message)
        except Exception as e:


            return render_template('index.html', result=f"Error processing file: {e}")

if __name__ == '__main__':
    app.run(debug=True)