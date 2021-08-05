from collections import defaultdict
from pathlib import Path

from .ui import *

class Bk():  # backgrounds
    def __init__(self, src, w, h):
        self.x, self.w, self.h = 0, w, h

        self.bk = defaultdict(str)
        for i in os.listdir(src):
            if i.startswith(('bk_')) and i.endswith(('jpg', 'png')):
                self.bk[i[3:-4]] = src + i

    def set(self, x):
        print('BK', x)
        self.x = x
        if x!=0 and x!='0': self.img = j_img(self.bk[x], self.w, self.h)

    def run(self, G):
        if self.x!=0 and self.x!='0': 
            G.screen.blit(self.img, (0, 0))
        else:
            G.screen.fill('black')

class Sound:
    def __init__(self, src):
        self.sd = defaultdict()
        for i in [src + f for f in os.listdir(src) if f.endswith(('mp3', 'wav'))]:
            now = pygame.mixer.Sound(i)
            now.set_volume(.5)
            self.sd[int(i[len(src)+2:-4])] = now

        # self.sd[0].set_volume(.3)
        # self.sd[21].set_volume(.2)

    def play(self, x):
        self.sd[x].play()


class Bgm:
    ing = now = 0
    def __init__(self, src):        # src: the music folder
        # self.bgms = [src + f for f in os.listdir(src) if f.endswith(('mp3', 'wav'))]
        self.bgms = defaultdict(str)
        for i in os.listdir(src):
            if i.endswith(('mp3', 'wav')):
                self.bgms[i[:-4]] = src + i
        self.player = pygame.mixer.music

    def set(self, x):
        if x=='0' or x==0: 
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
