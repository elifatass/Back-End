from fastapi import FastAPI
import os
import ast

app = FastAPI()

# 1. ANALİZ ZEKASI: Dosyanın içine bakıp hata arayan fonksiyon
def analyze_code(file_path):
    """Python dosyalarında gerçek yazım hatalarını bulur."""
    if not file_path.endswith(".py"):
        return [] # Şimdilik sadece Python dosyalarını analiz ediyoruz
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            ast.parse(code) # Python kodunu gramer olarak kontrol eder
            return [] # Hata yoksa boş liste
    except SyntaxError as e:
        # Eğer bir parantez unutulmuşsa veya yazım yanlışı varsa burası çalışır
        return [{
            "line": e.lineno,
            "message": f"Yazım Hatası: {e.msg}",
            "severity": "high"
        }]
    except Exception as e:
        return [{"line": 0, "message": str(e), "severity": "medium"}]

# 2. FORMATLAYICI: Ali Bulut'un "Altın Kuralı" (camelCase ve JSON yapısı)
def format_node(entry):
    # Dosya yolunu al ve analiz et
    errors = []
    status = "pending"
    
    if entry.is_file() and entry.name.endswith(".py"):
        errors = analyze_code(entry.path)
        status = "completed" if not errors else "error"

    return {
        "id": entry.path,
        "name": entry.name,
        "type": "folder" if entry.is_dir() else "file",
        "status": status,
        "errors": errors, # Bulunan hataları buraya ekliyoruz
        "children": []
    }

# 3. ENDPOINTLER (API Uç Noktaları)
@app.get("/")
async def root():
    return {"message": "AI Code Analyzer Sistemi Hazır", "status": "active"}

@app.get("/files")
async def list_files():
    root_path = "." 
    file_tree = []
    
    # Dosyaları tara, filtrele ve analiz et
    for entry in os.scandir(root_path):
        if entry.name.startswith(('.', 'venv', '__pycache__')):
            continue
        file_tree.append(format_node(entry))
        
    return file_tree

# Maildeki hata akışı simülasyonu için özel test ucu
@app.get("/scan-report")
async def get_scan_report():
    return {
        "event": "scan_completed",
        "scanner_version": "1.0.0",
        "results": await list_files()
    }
if