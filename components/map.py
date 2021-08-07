import pygame.draw

from .parts import *
from queue import PriorityQueue


class TileMap():
    def __init__(self, pos=(0, 0), size=(12, 24), tile_size=40):
        src = Path('resource/img/map')
        self.tiles = {
            name.stem: load_img(name, (tile_size, tile_size)) for name in src.rglob('*.jpg')
        }
        self.tile_size = tile_size
        self.w, self.h = size
        self.x, self.y = pos
        self.grid = [[0] * self.h for _ in range(self.w)]
        self.items = []
        self.screen = pygame.Surface((self.h * tile_size, self.w * tile_size))

        self.mouse_tile = pygame.Surface((tile_size, tile_size)).convert_alpha()
        self.mouse_tile.fill((10, 10, 10, 128))
        self.mx = self.my = 0

        self.select_tile = pygame.Surface((tile_size, tile_size)).convert_alpha()
        self.select_tile.fill((60, 40, 10, 128))
        self.select_cor = None
        self.selected = False

        self.btns = [
            Button(callback=self.click, visible=False,
                   pos=(self.x, self.y), size=(self.h * tile_size, self.w * tile_size))
        ]

        # test
        for i in range(self.w):
            for j in range(self.h):
                self.grid[i][j] = random.choice(list(self.tiles.values()))

    def pos2cor(self, pos, size=None, relative=True):
        ox, oy = (0, 0) if relative else (self.x, self.y)
        w, h = (0, 0) if size is None else size
        y = int((pos[0] - ox + 0.5 * h) // self.tile_size)
        x = int((pos[1] - oy + 0.5 * w) // self.tile_size)
        return [x, y]

    # pos to draw
    def cor2pos(self, cor, size=None, relative=True):
        ox, oy = (0, 0) if relative else (self.x, self.y)
        w, h = (0, 0) if size is None else size
        return [ox + (cor[1] + 0.5) * self.tile_size - 0.5 * w,
                oy + (cor[0] + 1) * self.tile_size - h]

    def draw_tile(self, sur, i, j):
        w, h = sur.get_size()
        x = (j + 0.5) * self.tile_size - 0.5 * w
        y = (i + 1) * self.tile_size - h
        self.screen.blit(sur, (x, y))

    def draw_item(self, gi, item):
        if isinstance(item, Animation):
            return item.run(gi)
        pos = (item.pos[0] - self.x, item.pos[1] - self.y)
        sur = item.img
        self.screen.blit(sur, pos)
        return True

    def draw_mouse(self, gi):
        self.mx, self.my = self.pos2cor(gi.mou_pos, relative=False)
        if 0 <= self.mx < self.w and 0 <= self.my < self.h:
            self.draw_tile(self.mouse_tile, self.mx, self.my)

    def draw_selected(self):
        if self.selected and self.select_cor is not None:
            self.draw_tile(self.select_tile, *self.select_cor)

    def draw_line(self):
        color = (82, 82, 81)
        width = 2
        for i in range(self.w + 1):
            pygame.draw.line(self.screen, color,
                             (0, i * self.tile_size),
                             (self.h * self.tile_size, i * self.tile_size),
                             width)
        for i in range(self.h + 1):
            pygame.draw.line(self.screen, color,
                             (i * self.tile_size, 0),
                             (i * self.tile_size, self.w * self.tile_size),
                             width)

    def draw(self, gi):
        for i in range(self.w):
            for j in range(self.h):
                self.draw_tile(self.grid[i][j], i, j)
        # self.draw_line()
        self.draw_selected()
        self.draw_mouse(gi)
        self.items = sorted([item for item in self.items if item.run(gi)])
        for item in self.items:
            item.map_cor = self.pos2cor(item.pos, item.size)
        gi.screen.blit(self.screen, (self.x, self.y))

    def add_item(self, item, cor=None):
        if cor is not None:
            item.pos = self.cor2pos(cor, item.size)
        item.map_cor = cor
        self.items.append(item)

    def click(self, gi):
        gi.players[gi.now_player].act(gi, params={'cor': (self.mx, self.my)})

    def run(self, gi):
        self.draw(gi)
        for btn in self.btns: btn.run(gi)
