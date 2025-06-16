from fastapi import FastAPI
from pydantic import BaseModel
import uuid, os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

app = FastAPI()

# Load DAMO pipeline
video_pipe = pipeline(
    Tasks.text_to_video_synthesis, 
    model='damo-vilab/modelscope-text-to-video-synthesis'
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_video(data: PromptRequest):
    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = f"/app/videos/{filename}"
    os.makedirs("/app/videos", exist_ok=True)

    # Generate video
    video_pipe({
        'text': data.prompt,
        'output_video': output_path
    })

    return {"video_path": output_path}
