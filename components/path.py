import os
from pathlib import Path

base_path = Path(os.path.realpath(__file__)).parent.parent
res_path = base_path / 'resource'
ani_path = res_path / 'animation'
img_path = res_path / 'img'
cha_path = res_path / 'character'