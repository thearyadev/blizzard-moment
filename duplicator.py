from pathlib import Path
import shutil
import uuid

dataset_dir = Path("./dataset")
DUPES = 250

for f in Path("./heroes").iterdir():
    target_dir = dataset_dir / f.name.replace(".png", "")
    target_dir.mkdir()
    for _ in range(DUPES):
        shutil.copy(str(f), str(target_dir / (uuid.uuid4().hex + ".png")))