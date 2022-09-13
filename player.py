import pygame
from entity import Entity
from settings import *
from support import import_folder


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load(
            './graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics
        self.import_player_assets()
        self.status = 'down'

        # movement
        self.attack = False
        self.attack_cd = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switch_weapon = True
        self.weapon_switch_cd = None
        self.switch_duration_cd = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.switch_magic = True
        self.magic_switch_cd = None

        # stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 6
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 100

        # damage
        self.vunerable = True
        self.hurt_time = None
        self.vunerability_cd = 500

    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def input(self):
        if not self.attack:
            keys = pygame.key.get_pressed()

            # move
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack
            if keys[pygame.K_SPACE]:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                print(self.weapon_index)

            # jutsu
            if keys[pygame.K_LCTRL]:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[
                    self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.switch_weapon:
                self.switch_weapon = False
                self.weapon_switch_cd = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.switch_weapon:
                self.switch_weapon = False
                self.weapon_switch_cd = pygame.time.get_ticks()
                if self.weapon_index == -1:
                    self.weapon_index = len(list(weapon_data.keys())) - 1
                else:
                    self.weapon_index -= 1

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_TAB] and self.switch_magic:
                self.switch_magic = False
                self.magic_switch_cd = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attack:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        # attack cooldown
        if self.attack:
            if current_time - self.attack_time >= self.attack_cd + weapon_data[self.weapon]['cooldown']:
                self.attack = False
                self.destroy_attack()

        if not self.switch_weapon:
            if current_time - self.weapon_switch_cd >= self.switch_duration_cd:
                self.switch_weapon = True

        # jutsus cooldown
        if not self.switch_magic:
            if current_time - self.magic_switch_cd >= self.switch_duration_cd:
                self.switch_magic = True

        if not self.vunerable:
            if current_time - self.hurt_time >= self.vunerability_cd:
                self.vunerable = True

    def animation(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # damage animations
        if not self.vunerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_weapon_dmg(self):
        base_dmg = self.stats['attack']
        weapon_dmg = weapon_data[self.weapon]['damage']
        return base_dmg + weapon_dmg

    def get_magic_dmg(self):
        base_dmg = self.stats['attack']
        magic_dmg = magic_data[self.magic]['strength']
        return base_dmg + magic_dmg

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animation()
        self.move(self.speed)
        self.energy_recovery()
