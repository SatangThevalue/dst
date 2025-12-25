import os
import json
import shutil
from pathlib import Path
from huggingface_hub import snapshot_download

class ModelManager:
    def __init__(self, config):
        self.base = Path(config['models']['base_path'])
        self.storage = self.base / config['models']['storage_dir']
        self.registry_path = self.base / config['models']['registry_file']
        
        self.storage.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()

    def _load_registry(self):
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=4)

    def list_models(self, tag_filter=None):
        if not tag_filter:
            return list(self.registry.keys())
        return [mid for mid, data in self.registry.items() if tag_filter in data.get('tags', [])]

    def download_model(self, model_id, tags=[]):
        safe_name = model_id.replace("/", "_")
        target_dir = self.storage / safe_name
        
        try:
            print(f"⬇️ Downloading {model_id}...")
            snapshot_download(repo_id=model_id, local_dir=target_dir)
            
            self.registry[model_id] = {
                "path": str(target_dir),
                "tags": tags,
                "type": "huggingface"
            }
            self._save_registry()
            return f"✅ Success: {model_id}", True
        except Exception as e:
            return f"❌ Error: {e}", False

    def delete_model(self, model_id):
        if model_id not in self.registry: return "Model not found"
        path = Path(self.registry[model_id]['path'])
        if path.exists(): shutil.rmtree(path)
        del self.registry[model_id]
        self._save_registry()
        return f"🗑️ Deleted {model_id}"

    def get_model_path(self, model_id):
        return self.registry.get(model_id, {}).get('path')