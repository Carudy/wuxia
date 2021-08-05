from .util import *


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
        self.items = defaultdict(list)
        self.screen = pygame.Surface((self.h * tile_size, self.w * tile_size))

        self.mouse_tile = pygame.Surface((tile_size, tile_size)).convert_alpha()
        self.mouse_tile.fill((10, 10, 10, 128))

        # test
        for i in range(self.w):
            for j in range(self.h):
                self.grid[i][j] = random.choice(list(self.tiles.values()))

    def pos2cor(self, pos):
        y = (pos[0] - self.x) // self.tile_size
        x = (pos[1] - self.y) // self.tile_size
        return (x, y)

    def draw_tile(self, sur, i, j):
        w, h = sur.get_size()
        x = (j + 0.5) * self.tile_size - 0.5 * w
        y = (i + 1) * self.tile_size - h
        self.screen.blit(sur, (x, y))

    def draw_item(self, item):
        pos = (item.pos[0] - self.x, item.pos[1] - self.y)
        sur = item.get_img()
        self.screen.blit(sur, pos)

    def draw_mouse(self, G):
        x, y = self.pos2cor(G.mou_pos)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.draw_tile(self.mouse_tile, x, y)

    def add_item(self, item):
        pos = self.pos2cor(item.pos)
        self.items[pos].append(item)

    def run(self, G):
        for i in range(self.w):
            for j in range(self.h):
                self.draw_tile(self.grid[i][j], i, j)
        self.draw_mouse(G)
        new_items = defaultdict(list)
        for i in range(self.w):
            for j in range(self.h):
                for item in self.items[(i, j)]:
                    if item.run(G):
                        self.draw_item(item)
                        pos = self.pos2cor(item.pos)
                        new_items[pos].append(item)
        self.items = new_items
        G.screen.blit(self.screen, (self.x, self.y))
