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

# Since main.py is INSIDE the 'app' folder, its directory IS the APP_PATH
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# 1. Serve index.html at the main URL (https://ar-webiste.onrender.com/)
@app.get("/")
async def serve_home():
    index_path = os.path.join(APP_PATH, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    # This helps you debug if the file is missing
    raise HTTPException(status_code=404, detail=f"index.html not found at {index_path}")

# 2. Automatically serve all models and images directly
# This makes them available at https://ar-webiste.onrender.com/filename.glb
app.mount("/static", StaticFiles(directory=APP_PATH), name="static")

# 3. Custom search logic for specific model requests
@app.get("/models/{file_name}")
async def get_model(file_name: str):
    search_name = file_name.lower().replace("naunt", "naut")
    
    if not os.path.exists(APP_PATH):
         raise HTTPException(status_code=500, detail="Directory not found")

    for existing_file in os.listdir(APP_PATH):
        if existing_file.lower() == search_name:
            file_path = os.path.join(APP_PATH, existing_file)
            
            # Proper media types for AR compatibility
            if existing_file.endswith(".glb"):
                return FileResponse(file_path, media_type="model/gltf-binary")
            if existing_file.endswith(".usdz"):
                return FileResponse(file_path, media_type="model/vnd.usd+zip")
            return FileResponse(file_path)
            
    raise HTTPException(status_code=404, detail="Model not found")