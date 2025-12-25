import torch
import gc
# 1. Rename import
from transformers import pipeline as hf_pipeline 

class AIEngine:
    def __init__(self, config, resource_manager, model_manager):
        self.rm = resource_manager
        self.mm = model_manager
        # 2. Rename attribute
        self.inference_pipeline = None 

    # 3. Rename method
    def load_model(self, model_id):
        path = self.mm.get_model_path(model_id)
        if not path: return "Model not found locally"
        
        # Clear VRAM
        self.inference_pipeline = None
        gc.collect()
        torch.cuda.empty_cache()

        device = "cuda:0" if self.rm.info['gpu'] else "cpu"
        dtype = torch.float16 if self.rm.info['gpu'] else torch.float32
        
        print(f"🚀 Activating model: {model_id} on {device}...")
        
        # ใช้ hf_pipeline ที่ rename มา
        self.inference_pipeline = hf_pipeline(
            "automatic-speech-recognition",
            model=path,
            device=device,
            torch_dtype=dtype
        )
        return "Model Activated"

    def transcribe(self, audio_path, model_id):
        # Auto load logic
        is_loaded = (
            self.inference_pipeline is not None and 
            self.inference_pipeline.model.name_or_path == self.mm.get_model_path(model_id)
        )

        if not is_loaded:
            self.load_model(model_id)
            
        try:
            res = self.inference_pipeline(audio_path)
            return res["text"]
        except Exception as e:
            return f"Error: {e}"