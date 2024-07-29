import whisperx
from logger import logger

MODEL = "large-v3"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

BATCH_SIZE = 8

model = whisperx.load_model(MODEL, DEVICE, compute_type=COMPUTE_TYPE)

def transcribe(audio_file: str) -> str:
    logger.info(f"Transcribing audio")
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=BATCH_SIZE)

    response = ""
    for segment in result["segments"]:
        response += f"{segment['text']}"
    return response