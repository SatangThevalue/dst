import yaml
import uvicorn
import gradio as gr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Import Modules
from src.core.resources import ResourceManager
from src.core.storage import StorageManager
from src.core.db import DBManager
from src.backend.model_manager import ModelManager
from src.backend.ai_engine import AIEngine
from src.ui.model_control import create_model_ui
from src.ui.audio import create_audio_ui

# 1. Init Config
load_dotenv()
with open("config/settings.yaml") as f: config = yaml.safe_load(f)

# 2. Init Systems
rm = ResourceManager()
mm = ModelManager(config)
ai = AIEngine(config, rm, mm)
storage = StorageManager(config, rm.is_colab)
db = DBManager(config)

# 3. FastAPI & PWA
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pwa_head = """
<link rel="manifest" href="/static/manifest.json">
<script>
    if('serviceWorker' in navigator) { navigator.serviceWorker.register('/static/service-worker.js'); }
</script>
"""

# 4. Gradio Interface
with gr.Blocks(title="DST Platform", theme=gr.themes.Soft(), head=pwa_head) as demo:
    gr.Markdown(f"# 🛠️ DST Platform (GPU: {rm.info['gpu_name']})")
    
    with gr.Tabs():
        with gr.Tab("🎙️ Audio Lab"):
            create_audio_ui(ai, storage, db, mm)
        with gr.Tab("🧠 Model Manager"):
            create_model_ui(mm)

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    if rm.is_colab:
        from pyngrok import ngrok
        print(f"🔗 Public URL: {ngrok.connect(8000).public_url}")
    
    print("🚀 Server starting at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)