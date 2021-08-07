from .parts import *


class Player:
    def __init__(self):
        self.action = 'select'
        self.selected_hero = None
        self.action_dict = {
            'select': self.select,
            'move': self.move,
            'attack': self.attack,
        }

    def act(self, gi, params):
        print(self.action)
        if self.action in self.action_dict:
            return self.action_dict[self.action](gi, params)

    def select(self, gi, params):
        gi.map.selected = True
        gi.map.select_cor = params['cor']
        self.selected_hero = None
        for i, hero in enumerate(gi.heroes):
            if tuple(hero.map_cor) == tuple(params['cor']):
                self.selected_hero = i
                self.action = 'attack'
                return
        self.selected_hero = None

    def move(self, gi, params):
        if self.selected_hero is None: return
        hero = gi.heroes[self.selected_hero]
        pos = gi.map.cor2pos(params['cor'], hero.size)
        hero.move_to(pos)
        gi.map.selected = False
        self.action = 'select'

    def attack(self, gi, params):
        if self.selected_hero is None: return
        hero = gi.heroes[self.selected_hero]
        hero.direction = 0 if params['cor'][1] >= hero.map_cor[1] else 1
        gi.map.add_item(Animation(name='attack', back=gi.map), cor=params['cor'])
        hero.animate('attack')
        gi.map.selected = False
        self.action = 'select'
