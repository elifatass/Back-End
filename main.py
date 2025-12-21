from fastapi import FastAPI
import os

app = FastAPI()

# Ali Bulut'un istediği JSON yapısını manuel hazırlayan fonksiyon
def format_node(entry):
    return {
        "id": entry.path,
        "name": entry.name,
        "type": "folder" if entry.is_dir() else "file",
        "status": "pending",
        "children": []
    }

@app.get("/")
async def root():
    return {"message": "Sistem Hazır", "url": "/files"}

@app.get("/files")
async def list_files():
    root_path = "." 
    file_tree = []
    
    # Dosyaları tara ve listele
    for entry in os.scandir(root_path):
        if entry.name.startswith(('.', 'venv', '__pycache__')):
            continue
        file_tree.append(format_node(entry))
        
    return file_tree

# Maildeki 2. madde: Hata örneği (Simülasyon)
@app.get("/test-error")
async def get_test_error():
    return {
        "event": "error_found",
        "data": {
            "fileId": "main.py",
            "errors": [
                {
                    "line": 10,
                    "message": "AI Simülasyonu: Potansiyel hata bulundu.",
                    "severity": "high"
                }
            ]
        }
    }