import pygame, re, random
from pathlib import Path
from collections import defaultdict
from .callbacks import *
from .path import *


def load_img(file, size=None):
    if size is None:
        return pygame.image.load(file)
    return pygame.transform.scale(pygame.image.load(file), size)


class Button:
    def __init__(self, img_src=None, txt=None, pos=[0, 0], visible=True,
                 size=(0, 0), key=None, callback=None, para=None, back=None):
        self.callback, self.para = callback, para
        self.size = size
        self.pos = pos
        self.key = key
        if key is not None:
            self.key = ord(self.key)

        self.visible = visible
        self.img = None
        self.back = back
        self.txt = txt
        if visible:
            if img_src is not None:
                self.img = load_img(img_src, size)
            elif size[0] > 0:
                self.img = pygame.Surface(size).convert_alpha()
                self.img.fill((120, 140, 160))
            else:
                self.img = None

            if self.img is not None:
                self.hover_sur = pygame.Surface(size).convert_alpha()
                self.hover_sur.fill((180, 170, 160, 66))

                if txt is not None:
                    cont = Label(txt, size=int(size[1] * 0.75))
                    _size = cont.cont.get_size()
                    self.img.blit(cont.cont, (0.5 * (self.size[0] - _size[0]), 0))

        self.cd = 0
        self.in_click = False

    def is_hover(self, mou_pos):
        ox, oy = self.back.pos if self.back is not None else (0, 0)
        _ok = self.pos[0] + ox < mou_pos[0] < self.pos[0] + self.size[0] + ox
        return _ok & (self.pos[1] + oy < mou_pos[1] < self.pos[1] + self.size[1] + oy)

    def is_click(self, mou_pos, moup, keyp):
        if self.key is not None and keyp[self.key]: return True
        return moup[0] and self.is_hover(mou_pos)

    def run(self, gi):
        # react
        self.cd = max(0, self.cd - gi.timep)
        if self.cd <= 0 and self.is_click(gi.mou_pos, gi.moup, gi.keyp) and self.callback is not None:
            if not self.in_click:
                if self.para is not None:
                    self.callback(gi, params=self.para)
                else:
                    self.callback(gi)
                self.cd = 100
                self.in_click = True
        else:
            self.in_click = False
        # draw
        if self.visible and self.img is not None and self.back is not None:
            self.back.screen.blit(self.img, self.pos)
            if self.is_hover(gi.mou_pos): self.back.screen.blit(self.hover_sur, self.pos)
        return True


class AnimationBase:
    def __init__(self, src, size=None):
        files = sorted(list(Path(src).rglob('*.png')))
        self.frames = []
        for file in files:
            self.frames.append(load_img(file, size))
        self.n = len(self.frames)

    def __getitem__(self, idx):
        return self.frames[idx]


class AnimationList:
    def __init__(self, src):
        self.animations = {}
        self.sizes = {}
        for ani in Path(src).iterdir():
            if ani.is_dir() and ani.stem[0].isalpha():
                self.animations[ani.stem] = AnimationBase(ani)
                self.sizes[ani.stem] = self.animations[ani.stem][0].get_size()

    def __len__(self):
        return len(self.animations)

    def __getitem__(self, idx):
        return self.animations[idx]


animation_list = AnimationList(src=ani_path / 'effect-png')


class Animation:
    def __init__(self, name, back, pos=(0, 0), loop=1, fps=18):
        self.name = name
        self.fid = 0
        self.pos = pos
        self.spf = 1000. / fps
        self.loop = loop
        self.looped = 0
        self.t = 0
        self.back = back
        self.size = animation_list[name][0].get_size()

    def run(self, gi):
        if self.fid >= animation_list[self.name].n:
            self.looped += 1
            self.fid = 0
            if 0 < self.loop <= self.looped:
                return False
        self.back.screen.blit(animation_list[self.name][self.fid], self.pos)
        self.t += gi.timep
        if self.t >= self.spf:
            self.t %= self.spf
            self.fid += 1
        return True

    def __le__(self, other):
        return self.pos[1] <= other.pos[1]

    def __lt__(self, other):
        return self.pos[1] < other.pos[1]


class Label:
    def __init__(self, txt, size=30, color=(0, 0, 0), pos=(0, 0),
                 font_family='microsoftyaheimicrosoftyaheiui'):
        self.font = pygame.font.SysFont(font_family, size)
        self.color = color
        self.cont = self.font.render(txt, True, color)
        self.pos = pos

    def set(self, txt):
        self.cont = self.font.render(txt, True, self.color)

    def run(self, gi):
        gi.screen.blit(self.cont, self.pos)


class Label_row():
    def __init__(self, txt, lenth=31, size=30, color=(0, 0, 0), pos=(0, 0),
                 font_family='microsoftyaheimicrosoftyaheiui'):
        self.font = pygame.font.SysFont(font_family, size)
        self.px, self.py = pos
        self.font_size = size

        lines = re.findall('.{' + str(lenth) + '}', txt)
        lines.append(txt[(len(lines) * lenth):])
        self.lines = [self.font.render(x, True, color) for x in lines]

    def set_pos(self, px, py):
        self.px, self.py = px, py

    def run(self, gi):
        for i in range(len(self.lines)):
            gi.screen.blit(self.lines[i], (self.px, self.py + (self.font_size * 1.23) * i))
