from collections import defaultdict

import pygame

from .ui import *


def drt(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


class BaseBar:
    def __init__(self, size, color, back, pos=(0, 0)):
        self.size = size
        self.pos = pos
        self.screen = pygame.Surface(self.size).convert_alpha()
        self.screen.fill(color)
        self.back = back
        self.items = []

    def before(self, gi):
        pass

    def run(self, gi):
        self.before(gi)
        for i in self.items: i.run(gi)
        self.back.screen.blit(self.screen, self.pos)
        return True


class TopBar(BaseBar):
    def __init__(self, size, pos, back):
        super(TopBar, self).__init__(size=size, pos=pos, back=back, color=(123, 125, 112))


class SelectedBar(BaseBar):
    def __init__(self, size, pos, back):
        super(SelectedBar, self).__init__(size=size, pos=pos, color=(165, 154, 61), back=back)

    def before(self, gi):
        hero = gi.players[gi.now_player].selected_hero
        if hero is not None:
            hero = gi.heroes[hero]
            self.screen.blit(hero.head, (4, 4))


class BottomBar(BaseBar):
    def __init__(self, size=(960, 100), pos=(0, 0), back=None):
        super(BottomBar, self).__init__(size=size, pos=pos, back=back, color=(103, 105, 102))
        self.items = [
            SelectedBar(size=(size[0] * 0.25, size[1] * 0.9), pos=(5, size[1] * 0.05), back=self),
            Button(visible=False, key='z', back=self, callback=test),
        ]


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
