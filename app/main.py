import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# Read configuration from environment variables
MODEL_ID   = os.getenv("MODEL_ID", "damo-vilab/modelscope-text-to-video-synthesis")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/videos")
DEVICE     = os.getenv("CUDA_DEVICE", "cpu")

# Initialize FastAPI
app = FastAPI()

# Initialize DAMO pipeline
try:
    video_pipe = pipeline(
        Tasks.text_to_video_synthesis,
        model=MODEL_ID,
        device=DEVICE
    )
except Exception as e:
    raise RuntimeError(f"Failed to load pipeline for model {MODEL_ID}: {e}")

# Pydantic model for request body
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate", status_code=201)
async def generate_video(data: PromptRequest):
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Run generation
    try:
        video_pipe({
            'text': data.prompt,
            'output_video': output_path
        })
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

    # Verify file creation
    if not os.path.isfile(output_path):
        raise HTTPException(status_code=500, detail="Video generation failed, no output file found.")

    return {"video_path": output_path}
