import os
from pathlib import Path

class StorageManager:
    def __init__(self, config, is_colab):
        # ปรับ Path ตาม Environment
        root = Path("/content/drive/MyDrive/DST_Data") if is_colab else Path("./data")
        self.audio_dir = root / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def list_audio(self):
        # สร้างไฟล์หลอกๆ เพื่อทดสอบ
        if not list(self.audio_dir.glob("*.wav")):
            import soundfile as sf
            import numpy as np
            sr = 16000
            audio = np.random.uniform(-1, 1, sr*3)
            sf.write(str(self.audio_dir / "test_sample.wav"), audio, sr)
            
        return sorted([f.name for f in self.audio_dir.glob("*.wav")])

    def get_path(self, filename):
        return str(self.audio_dir / filename)