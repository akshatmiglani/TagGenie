import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
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


transcribed_text = read_text_from_file("transcribe.txt")
tags_response = generate_tags_chat(transcribed_text)

response_message = tags_response.choices[0].message.content
print(response_message)


with open("tags.txt","w") as f:
    f.write(response_message)