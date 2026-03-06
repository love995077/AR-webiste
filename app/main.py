import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Enable CORS so the main website can access these models
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use the 'app' folder where your index.html and models are located
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, "app")

@app.get("/{file_name}")
async def get_model(file_name: str):
    # Your fuzzy search logic for typos
    search_name = file_name.lower().replace("naunt", "naut")
    
    if not os.path.exists(app_path):
         raise HTTPException(status_code=500, detail="App folder not found")

    for existing_file in os.listdir(app_path):
        if existing_file.lower() == search_name:
            file_path = os.path.join(app_path, existing_file)
            
            # Set headers correctly for iPhone/Android compatibility
            if existing_file.endswith(".glb"):
                return FileResponse(file_path, media_type="model/gltf-binary")
            if existing_file.endswith(".usdz"):
                return FileResponse(file_path, media_type="model/vnd.usd+zip")
            return FileResponse(file_path)
            
    raise HTTPException(status_code=404, detail="Model not found")

# Serve the index.html as the home page
@app.get("/")
async def serve_home():
    return FileResponse(os.path.join(app_path, "index.html"))