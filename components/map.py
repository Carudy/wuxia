from .util import *

class TileMap():
	def __init__(self, pos=(0, 0), size=(12, 24), tile_size=32):
		src = Path('resource/img/map')
		self.tiles = {
			name.stem : load_img(name) for name in src.rglob('*.jpg')
		}
		self.tile_size = tile_size
		self.w, self.h = size
		self.x, self.y = pos
		self.layers = []
		self.screen = pygame.Surface((self.h*tile_size, self.w*tile_size))

		self.mouse_tile = pygame.Surface((tile_size, tile_size)).convert_alpha()
		self.mouse_tile.fill((10, 10, 10, 128))

		layer = [[0] * self.h for _ in range(self.w)]
		for i in range(self.w):
			for j in range(self.h): 
				layer[i][j] = random.choice(list(self.tiles.values()))
		self.layers.append(layer)

	def draw_tile(self, G, sur, i, j):
		w, h = sur.get_size()
		x = (j+0.5)*self.tile_size - 0.5*w
		y = (i+1)*self.tile_size - h
		self.screen.blit(sur, (x, y))

	def draw_mouse_tile(self, G):
		y = G.mou_pos[0] // self.tile_size
		x = G.mou_pos[1] // self.tile_size
		if 0 <= x < self.w and 0 <= y < self.h:
			self.draw_tile(G, self.mouse_tile, x, y)

	def run(self, G):
		for layer in self.layers:
			for i in range(self.w):
				for j in range(self.h):
					self.draw_tile(G, layer[i][j], i, j)
		self.draw_mouse_tile(G)
		G.screen.blit(self.screen, (self.x, self.y))