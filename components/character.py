from .parts import *


class Character:
    def __init__(self, src, pos=[0, 0], size=None, fps=12):
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
        self.status = 'attack'
        self.fid = 0
        self.pos = pos
        self.spf = 1000. / fps
        self.t = 0
        self.moving = False
        self.tar_pos = None
        self.speed = 0.25
        self.direction = 0
        self.map_cor = None

        # -1 for no-camp
        self.camp = -1

    @property
    def img(self):
        ret = self.imgs[self.status]
        if isinstance(ret, AnimationBase):
            ret = ret[self.fid]
        if self.direction == 1:
            return pygame.transform.flip(ret, True, False)
        return ret

    def animate(self, name):
        if self.status == name: return
        self.status = name
        self.fid = self.t = 0

    def handle_animation(self, gi):
        if self.status != 'stand':
            self.t += gi.timep
            if self.t >= self.spf:
                self.t %= self.spf
                self.fid += 1
            if self.fid >= self.imgs[self.status].n:
                self.status = 'stand'

    def move_to(self, pos):
        if pos == self.pos: return
        self.tar_pos = pos
        self.moving = True

    def move(self, gi):
        if not self.moving: return
        dx = drt(self.tar_pos[0] - self.pos[0])
        dy = drt(self.tar_pos[1] - self.pos[1])
        self.direction = 0 if dx > 0 else 1
        nx = self.pos[0] + dx * self.speed * gi.timep
        ny = self.pos[1] + dy * self.speed * gi.timep
        if drt(self.tar_pos[0] - self.pos[0]) * drt(nx - self.tar_pos[0]) >= 0: nx = self.tar_pos[0]
        if drt(self.tar_pos[1] - self.pos[1]) * drt(ny - self.tar_pos[1]) >= 0: ny = self.tar_pos[1]
        self.pos = [nx, ny]
        if self.pos == self.tar_pos:
            self.moving = False

    def run(self, gi):
        self.handle_animation(gi)
        self.move(gi)
        return True
