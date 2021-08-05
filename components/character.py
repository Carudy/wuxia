from .ui import *


class Character:
    def __init__(self, src, pos=[0, 0], size=None):
        src = Path(src)
        self.imgs = {
            'stand': load_img(src / 'stand.png')
        }
        for folder in src.iterdir():
            if folder.is_dir():
                self.imgs[folder.stem] = AnimationBase(folder, size)

        if size is None:
            self.size = self.imgs['stand'].get_size()
        else:
            self.size = size
        self.status = 'stand'
        self.fid = 0
        self.pos = pos

    def get_img(self):
        ret = self.imgs[self.status]
        if isinstance(ret, AnimationBase):
            return ret[self.fid]
        else:
            return ret

    def run(self, G):
        return True
