from player import Player
from support import *
from settings import *
from random import choice
from weapon import Weapon
from UI import UI
from enemy import Enemy
import random

class Level:
    def __init__(self):
        # screen
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # user interface
        self.ui = UI()

        self.setup()

    def setup(self):
        self.player = Player((360, 360), [self.all_sprites], self.create_attack, self.destroy_attack)
        # self.enemy = Enemy((random.choice([-100, SCREEN_WIDTH + 100]), random.choice([-100, SCREEN_HEIGHT + 100])),
                           # z[self.all_sprites, self.attackable_sprites])

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.all_sprites])
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, True)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.kill()

    def run(self, dt):
        self.display_surface.fill('olive')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.player_attack_logic()
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.update(self, self.player, self.attack_sprites if self.player.attack else 0)
        self.ui.display(self.player)