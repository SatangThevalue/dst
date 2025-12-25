import torch, psutil, sys

class ResourceManager:
    def __init__(self):
        self.is_colab = "google.colab" in sys.modules
        self.info = {
            "gpu": torch.cuda.is_available(),
            "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None",
            "ram": round(psutil.virtual_memory().total / (1024**3), 2)
        }