import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Enable CORS for cross-device access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Since main.py is INSIDE the 'app' folder, its directory IS where everything lives
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# 1. Serve index.html as the primary landing page
@app.get("/")
async def serve_home():
    index_path = os.path.join(APP_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found")

# 2. Custom search logic for specific model requests (Used by your AR buttons)
@app.get("/models/{file_name}")
async def get_model(file_name: str):
    search_name = file_name.lower().replace("naunt", "naut")
    
    for existing_file in os.listdir(APP_PATH):
        if existing_file.lower() == search_name:
            file_path = os.path.join(APP_PATH, existing_file)
            
            # Critical headers for iPhone/Android AR
            if existing_file.endswith(".glb"):
                return FileResponse(file_path, media_type="model/gltf-binary")
            if existing_file.endswith(".usdz"):
                return FileResponse(file_path, media_type="model/vnd.usd+zip")
            return FileResponse(file_path)
            
    raise HTTPException(status_code=404, detail="Model file not found")

# 3. Serve everything else (images, models, etc.) from the root
# This ensures a request for "/Astronaut.glb" actually finds the file
app.mount("/", StaticFiles(directory=APP_PATH), name="static")