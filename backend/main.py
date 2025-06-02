from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import base64
from PIL import Image
import io

app = FastAPI(title="Image Caption Generator API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Image Caption Generator API with LLaVA"}

@app.post("/caption/")
async def caption_image(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and validate image
        image_bytes = await file.read()
        
        # Verify it's a valid image
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # Verify it's a valid image
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Convert to base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Send request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": "Describe this image in detail. Provide a comprehensive and descriptive caption.",
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=60  # Longer timeout for image processing
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error communicating with Ollama")
        
        result = response.json()
        caption = result["response"].strip()
        
        return {
            "filename": file.filename,
            "caption": caption,
            "file_size": len(image_bytes)
        }
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/caption/custom/")
async def caption_image_custom(file: UploadFile = File(...), prompt: str = "Describe this image"):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and validate image
        image_bytes = await file.read()
        
        # Verify it's a valid image
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Convert to base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Send request to Ollama with custom prompt
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error communicating with Ollama")
        
        result = response.json()
        caption = result["response"].strip()
        
        return {
            "filename": file.filename,
            "prompt": prompt,
            "caption": caption,
            "file_size": len(image_bytes)
        }
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
def health_check():
    try:
        # Test connection with Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            tags = response.json()
            models = [model["name"] for model in tags.get("models", [])]
            llava_available = any("llava" in model for model in models)
            return {
                "status": "healthy", 
                "ollama": "connected",
                "llava_available": llava_available,
                "available_models": models
            }
        else:
            return {"status": "unhealthy", "ollama": "disconnected"}
    except:
        return {"status": "unhealthy", "ollama": "disconnected"}