from components import *


class GameInstance:
    def __init__(self, width=980, height=800):
        # display
        pygame.display.init()
        # pygame.display.set_caption("Game")
        # os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (280, 120)
        pygame.init()
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        self.screen.fill((23, 19, 11))
        self.clock = pygame.time.Clock()

        self.map = TileMap(pos=(10, 100))
        self.heroes = [
            Character(cha_path / '小虾米', back=self.map),
            Character(cha_path / '石破天', back=self.map),
        ]
        for i, hero in enumerate(self.heroes):
            self.map.add_item(hero, cor=[i + 2, i + 2])

        self.now_player = 0
        self.players = [
            Player(),
        ]

        self.items = [
            TopBar(pos=(10, 5), size=(960, 90), back=self),
            BottomBar(pos=(10, 590), size=(960, 200), back=self),
        ]

    def run(self):
        self.timep = self.clock.tick(60)
        self.keyp = pygame.key.get_pressed()
        self.moup = pygame.mouse.get_pressed()
        self.mou_pos = pygame.mouse.get_pos()

        self.map.run(self)
        self.items = [i for i in self.items if i.run(self)]
        self.heroes = [i for i in self.heroes if i.run(self)]


# ******************************** loop ***************************************************
if __name__ == '__main__':
    gi = GameInstance()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        gi.run()
        pygame.display.update()
