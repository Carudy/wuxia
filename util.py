import os, pygame, socket, string, re, random
from pygame.locals import *
from collections import defaultdict as dd
#******************** tool func **************************   
# def p_img(file, w, h):
#     return pygame.transform.scale(pygame.image.load(file), (w, h))

# def j_img(file, w, h):
#     return pygame.transform.scale(pygame.image.load(file), (w, h))
def load_img(file, w=0, h=0):
    if w==0: return pygame.image.load(file)
    return pygame.transform.scale(pygame.image.load(file), (w, h))
#******************* classes ************************** 
class Bk():  # backgrounds
    def __init__(self, src, w, h):
        self.x, self.w, self.h = 0, w, h

        self.bk = dd(str)
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


class Button():
    def __init__(self, i=-1, txt='', ts=34, color=(0, 0, 0), pos=(0, 0), w=0, h=0, key=0, f=None, para=None):
        self.key, self.f, self.w, self.h, self.pos  = key, f, w, h, pos
        self.img, self.txt, self.para = None, txt, para
        if i>=0:
            if w==0: self.w, self.h = len(txt) * (ts+2), (ts+14)
            self.img = p_img('img/btn'+str(i)+'.png', self.w, self.h)
            tx = pos[0] + (self.w - len(txt) * ts) * 0.5
            ty = pos[1] + (self.h - ts) * 0.5
            self.cont0 = Label(txt, size=ts, pos=(tx, ty), color=color)
            self.cont1 = Label(txt, size=ts, pos=(tx, ty), color=(255, 204, 22))

        self.cd=0
        if isinstance(self.key, str): self.key=ord(self.key)

    def mouse_in(self, mou_pos):
        _ok  = mou_pos[0] > self.pos[0] and mou_pos[0] < self.pos[0]+self.w
        return _ok & (mou_pos[1] > self.pos[1] and mou_pos[1] < self.pos[1]+self.h)

    def ok(self, mou_pos, moup, keyp):
        if self.key>0 and keyp[self.key]: return True
        return moup[0] and self.mouse_in(mou_pos)

    def run(self, G):
        self.cd = max(0, self.cd-G.timep)
        if self.f and self.cd <=0 and self.ok(G.mou_pos, G.moup, G.keyp):
            # G.sound.play(27)
            self.cd = 250
            if self.para is not None:
                self.f(G, self.para)
            else:
                self.f(G)
        if self.img is not None:
            G.screen.blit(self.img, self.pos)
            if self.mouse_in(G.mou_pos):
                self.cont1.run(G)
            else:
                self.cont0.run(G)


class Label():
    def __init__(self, txt, size=30, color=(0, 0, 0), pos=(0, 0), font_family=0):
        if font_family==0:
            self.font = pygame.font.Font('font/hanyi.ttf', size)
        else:
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

class Sound:
    def __init__(self, src):
        self.sd = dd()
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
        self.bgms = dd(str)
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
