from collections import defaultdict

from .ui import *


def drt(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


class TopBar:
    def __init__(self, size=(960, 80), pos=(0, 0)):
        self.size = size
        self.pos = pos
        self.img = pygame.Surface(size).convert_alpha()
        self.img.fill((123, 125, 112))

    def run(self, gi):
        gi.screen.blit(self.img, self.pos)


class BottomBar:
    def __init__(self, size=(960, 100), pos=(0, 0)):
        self.size = size
        self.pos = pos
        self.screen = pygame.Surface(size).convert_alpha()
        self.screen.fill((103, 105, 102))
        self.items = [
            Button(pos=[10, 10], size=(100, 40), txt='更换', key='z', back=self),
        ]

    def run(self, gi):
        for i in self.items:
            i.run(gi)
        gi.screen.blit(self.screen, self.pos)
        return True


class Sound:
    def __init__(self, src):
        self.sd = defaultdict()
        for i in [src + f for f in os.listdir(src) if f.endswith(('mp3', 'wav'))]:
            now = pygame.mixer.Sound(i)
            now.set_volume(.5)
            self.sd[int(i[len(src) + 2:-4])] = now

        # self.sd[0].set_volume(.3)
        # self.sd[21].set_volume(.2)

    def play(self, x):
        self.sd[x].play()


class Bgm:
    ing = now = 0

    def __init__(self, src):
        self.bgms = defaultdict(str)
        for i in os.listdir(src):
            if i.endswith(('mp3', 'wav')):
                self.bgms[i[:-4]] = src + i
        self.player = pygame.mixer.music

    def set(self, x):
        if x == '0' or x == 0:
            self.pause()
            return
        if self.now == x: return
        self.now = x
        self.ing = 1
        self.player.stop()
        self.player.load(self.bgms[x])
        self.player.play(-1)

    def play(self):
        self.ing = 1
        self.player.play(-1)

    def pause(self):
        if self.ing == 1:
            self.ing = 0
            self.player.pause()
        else:
            self.ing = 1
            self.player.unpause()
