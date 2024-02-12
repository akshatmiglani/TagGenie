import whisper

model = whisper.load_model("base")
result=model.transcribe("output.wav")

with open("transcribe.txt","w") as f:
    f.write(result["text"])
