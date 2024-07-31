# Flask Video to Text Application

This Flask application converts a video file to text and generates tags based on the extracted text. It uses MoviePy to extract audio from the video, Whisper for speech-to-text transcription, and Gemini API for generating tags.

## Overview

1. **MoviePy**: A Python library used for video editing, including extracting audio from video files.
2. **Whisper**: An automatic speech recognition (ASR) model by OpenAI, used to transcribe audio to text.
3. **Gemini API**: Google's generative AI service used for generating text, including extracting keywords from the transcribed text.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Flask
- MoviePy
- Whisper
- Google Generative AI (Gemini API)
- Python dotenv

You can install the required packages using pip:

```bash
pip install flask moviepy openai google-generativeai python-dotenv
```

## Configuration

1. **Create a `.env` file** in the project directory with the following content:

    ```dotenv
    GOOGLE_API_KEY=your_google_api_key
    ```

    Replace `your_google_api_key` with your actual Google API key.

2. **Set up Whisper**: Ensure that the Whisper model is available for transcription. You might need to install it if it’s not already available.

## Application Structure

- **app.py**: The main Flask application script.
- **templates/index.html**: The HTML form for uploading video files.

## How It Works

1. **Upload a Video**: Use the web form to upload a video file.
2. **Video to Audio**: The application extracts the audio from the video using MoviePy.
3. **Audio to Text**: The audio file is transcribed into text using Whisper.
4. **Generate Tags**: The transcribed text is processed to extract keywords using Gemini API.
5. **Display Results**: The generated tags are displayed on the webpage.

## Usage

1. **Run the Application**:

    ```python
    python app.py
    ```

2. **Access the Web Interface**:

    Open a web browser and go to `http://127.0.0.1:5000/`.

3. **Upload a Video File**:

    - Choose a video file and submit it through the form.
    - The application processes the file and displays the generated tags.

## Code Explanation

- **`read_text_from_file(file_path)`**: Reads the content of a text file.
- **`video_to_audio(video_path, audio_path)`**: Converts video to audio using MoviePy.
- **`audio_to_text(audio_path)`**: Transcribes audio to text using Whisper.
- **`generate_tags_chat(prompt_text)`**: Uses Gemini API to generate keywords from the transcribed text.
