import os, pygame, string, re, random
from pygame.locals import *

def load_img(file, w=0, h=0):
    if w==0: return pygame.image.load(file)
    return pygame.transform.scale(pygame.image.load(file), (w, h))


class Button():
    def __init__(self, img_src=None, txt=None, pos=(0, 0), 
                 size=None, key=None, callback=None, para=None):
        self.callback, self.para = callback, para
        self.size = size
        self.pos  = pos
        self.key  = key
        if key is not None:
            self.key=ord(self.key)

        if img_src is not None:
            self.img = load_img(img_src, *size)
        elif size is not None:
            self.img = pygame.Surface(size).convert_alpha()
            self.img.fill((12, 16, 19))
        else:
            self.img = None

        if self.img is not None:
            self.hover_sur = pygame.Surface(size).convert_alpha()
            self.hover_sur.fill((180, 170, 160, 66))

        if txt is not None:
            self.txt = txt
            self.cont = Label(txt, size=int(size[1]*0.8), pos=(pos[0]+2, pos[1]+2))
        self.cd = 0
        self.in_click = False

    def is_hover(self, mou_pos):
        _ok  = mou_pos[0] > self.pos[0] and mou_pos[0] < self.pos[0]+self.size[0]
        return _ok & (mou_pos[1] > self.pos[1] and mou_pos[1] < self.pos[1]+self.size[1])

    def is_click(self, mou_pos, moup, keyp):
        if self.key is not None and keyp[self.key]: return True
        return moup[0] and self.is_hover(mou_pos)

    def run(self, G):
        self.cd = max(0, self.cd-G.timep)
        if self.cd <=0 and self.is_click(G.mou_pos, G.moup, G.keyp) and self.callback is not None:
            if not self.in_click:
                if self.para is not None:
                    self.callback(G, **self.para)
                else:
                    self.callback(G)
                self.cd = 100
                self.in_click = True
        else:
            self.in_click = False
        if self.img is not None:
            G.screen.blit(self.img, self.pos)
            if self.is_hover(G.mou_pos): G.screen.blit(self.hover_sur, self.pos)
            if self.cont: self.cont.run(G)


class Label():
    def __init__(self, txt, size=30, color=(0, 0, 0), pos=(0, 0), font_family='microsoftyaheimicrosoftyaheiui'):
        self.font = pygame.font.SysFont(font_family, size)
        self.color = color
        self.cont = self.font.render(txt, True, color)
        self.pos = pos

    def set(self, txt):
        self.cont = self.font.render(txt, True, self.color)

    def run(self, G):
        G.screen.blit(self.cont, self.pos)


class Label_bar():
    def __init__(self, txt, img, size=30, color=(0, 0, 0), pos=(0, 0), font_family=0):
        w, h = len(txt) * (size+2), (size+14)
        self.src = img
        self.img = p_img(img, w, h)
        self.pos, self.size = pos, size
        tx = pos[0] + (w - len(txt) * size) * 0.5
        ty = pos[1] + (h - size) * 0.4
        self.txt = Label(txt, size, color, (tx, ty), font_family)

    def set(self, txt):
        self.txt.set(txt)
        w, h = len(txt) * (self.size+2), (self.size+14)
        tx = self.pos[0] + (w - len(txt) * self.size) * 0.5
        ty = self.pos[1] + (h - self.size) * 0.4
        self.txt.pos = (tx, ty)
        w, h = len(txt) * (self.size+2), (self.size+14)
        self.img = p_img(self.src, w, h)

    def run(self, G):
        G.screen.blit(self.img, self.pos)
        self.txt.run(G)


class Label_row():
    def __init__(self, txt, lenth=31, size=30, color=(0, 0, 0), pos=(0, 0), font_family='microsoftyaheimicrosoftyaheiui'):
        self.font = pygame.font.SysFont(font_family, size)
        self.px, self.py = pos
        self.font_size = size

        lines = re.findall('.{' + str(lenth) + '}', txt)
        lines.append(txt[(len(lines)*lenth):])
        self.lines = [self.font.render(x, True, color) for x in lines]

    def set_pos(self, px, py):
        self.px, self.py = px, py

    def run(self, G):
        for i in range(len(self.lines)):
            G.screen.blit(self.lines[i], (self.px, self.py + (self.font_size * 1.23)*i))