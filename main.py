from pathlib import Path
from components import *

class GameInstance():
	def __init__(self, width=768, height=600):
		# display
		pygame.display.init()
		# pygame.display.set_caption("Game")
		# os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (280, 120)
		pygame.init()
		# pygame.mixer.pre_init(44100, 16, 2, 4096)
		self.size       =   (width, height)
		self.screen     =   pygame.display.set_mode(self.size, 0, 32)
		self.clock      =   pygame.time.Clock()
		self.map  		=	TileMap()
		self.btns 		=   [
			Button(size=(100, 40), txt='更换地图')
		]

		self.run_list	= [self.map, self.btns]

	def recurve_run(self, x):
		if isinstance(x, list):
			for mono in x: self.recurve_run(mono)
		else:
			x.run(self)

	def run(self):
		self.timep = self.clock.tick(60)
		self.keyp    =  pygame.key.get_pressed()
		self.moup    =  pygame.mouse.get_pressed()
		self.mou_pos =  pygame.mouse.get_pos()
		self.recurve_run(self.run_list)


G = GameInstance()
#******************************** loop ***************************************************
if __name__ == '__main__': 
	# main loop
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		G.run()
		pygame.display.update()