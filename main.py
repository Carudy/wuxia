from components import *


def test(G):
    G.xm.pos[0] += 5


class GameInstance:
    def __init__(self, width=960, height=600):
        # display
        pygame.display.init()
        # pygame.display.set_caption("Game")
        # os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (280, 120)
        pygame.init()
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        self.clock = pygame.time.Clock()
        self.animations = AnimationList(src='resource/animation/effect-png')

        self.map = TileMap()
        self.xm = Character('resource/character/xiami', pos=[100, 100])
        self.map.add_item(self.xm)

        self.items = [
            Button(size=(100, 40), txt='更换', pos=[0, 500], callback=test, key='z'),
            Animation('attack', (100, 100)),
        ]

    def run(self):
        self.timep = self.clock.tick(60)
        self.keyp = pygame.key.get_pressed()
        self.moup = pygame.mouse.get_pressed()
        self.mou_pos = pygame.mouse.get_pos()

        self.map.run(self)
        self.items = [i for i in self.items if i.run(self)]


# ******************************** loop ***************************************************
if __name__ == '__main__':
    G = GameInstance()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        G.run()
        pygame.display.update()
