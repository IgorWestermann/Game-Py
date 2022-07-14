import pygame
from settings import *


class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 10), 3)

    def selecion_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched == True:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 3)

        return bg_rect

    def selecion_box_aux(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE *
                              0.7, ITEM_BOX_SIZE * 0.7)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # if has_switched == True:
        #     pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        # else:
        #     pygame.draw.rect(self.display_surface,
        #                      UI_BORDER_COLOR_ACTIVE, bg_rect, 3)

        return bg_rect

    def weapon_orverlay(self, weapon_index, has_switched):
        bg_rect = self.selecion_box(90, 615, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def next_weapon_orverlay(self, weapon_index):
        bg_rect = self.selecion_box_aux(25, 627)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)
        if weapon_index < len(list(weapon_data.keys())) - 1:
            weapon_index += 1
        else:
            weapon_index = 0

    def previous_weapon_orverlay(self, weapon_index):
        bg_rect = self.selecion_box_aux(180, 627)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selecion_box(1100, 615, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        # self.selecion_box(120, 615)
        self.weapon_orverlay(player.weapon_index, player.switch_weapon)
        self.next_weapon_orverlay(player.weapon_index + 1)
        self.previous_weapon_orverlay(player.weapon_index - 1)
        self.magic_overlay(player.magic_index, player.switch_magic)
        # self.show_exp(player.exp)
