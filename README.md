# DAMO Text-to-Video Service

Runs Alibaba DAMO's text-to-video model using FastAPI. Deployable to Render for free.

## Usage

POST `/generate` with JSON:
```json
{ "prompt": "a cat surfing on a wave" }
