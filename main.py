import os
import pygame
import sys
import math
import random

from setting import *
from button import ImageButton
from set import SettingsScene, generate_click
from game import GameScene
from intro import IntroScene
from assets import load_scaled, make_circle_crop, draw_overlay, draw_panel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def project_path(*parts):
    return os.path.join(BASE_DIR, *parts)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

try:
    pygame.mixer.music.load(project_path("laguu.ogg"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception:
    pass

click_sfx = generate_click()

bg        = load_scaled(project_path("asset", "kantor.jpeg"), WIDTH, HEIGHT)
logo_raw  = load_scaled(project_path("asset", "logo game.jpeg"), 220, 220)
logo      = make_circle_crop(logo_raw, 220)
menu_font = pygame.font.SysFont("Georgia", 20, bold=True)
small_font = pygame.font.SysFont("Georgia", 14)
label_font = pygame.font.SysFont("Georgia", 18, bold=True)


class Particle:

    def __init__(self):
        self.reset(random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def reset(self, x=None, y=None):
        self.x       = x if x is not None else random.randint(0, WIDTH)
        self.y       = y if y is not None else HEIGHT + 5
        self.size    = random.uniform(0.6, 2.8)
        self.speed   = random.uniform(0.08, 0.55)
        self.alpha   = random.randint(30, 100)
        self.drift   = random.uniform(-0.25, 0.25)
        self.flicker = random.uniform(0, math.pi * 2)

    def update(self, tick):
        self.y -= self.speed
        self.x += math.sin(tick * 0.012 + self.flicker) * 0.25 + self.drift
        if self.y < -5:
            self.reset()

    def draw(self, surface, tick):
        a  = int(self.alpha + math.sin(tick * 0.05 + self.flicker) * 16)
        a  = max(0, min(255, a))
        sz = int(self.size * 2 + 1)
        s  = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(s, (215, 208, 198, a), (int(self.size), int(self.size)), int(self.size))
        surface.blit(s, (int(self.x), int(self.y)))


particles = [Particle() for _ in range(150)]


def make_menu_btn(base, hov):
    def _s(c, a):
        s = pygame.Surface((360, 54), pygame.SRCALPHA)
        pygame.draw.rect(s, (*c, a), s.get_rect(), border_radius=27)
        pygame.draw.rect(s, (255, 220, 80, 90), s.get_rect(), border_radius=27, width=1)
        return s
    return _s(base, 180), _s(hov, 220)


bn, bh = make_menu_btn((18, 18, 18), (52, 52, 52))

settings_scene = SettingsScene()
game_scene     = GameScene()
bx             = WIDTH // 2
play_btn       = ImageButton(bn, bh, bx, 440, "MULAI MISI",   menu_font)
setting_btn    = ImageButton(bn, bh, bx, 504, "PENGATURAN",   menu_font)
exit_btn       = ImageButton(bn, bh, bx, 568, "KELUAR",       menu_font)

IntroScene().run(screen)

tick    = 0
running = True

while running:
    clock.tick(FPS)
    tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if exit_btn.is_clicked(event):
            click_sfx.play()
            running = False
        if play_btn.is_clicked(event):
            click_sfx.play()
            game_scene.run(screen)
        if setting_btn.is_clicked(event):
            click_sfx.play()
            settings_scene.run(screen)
            screen = pygame.display.get_surface()

    screen.blit(bg, (0, 0))
    draw_overlay(screen, 60)

    for p in particles:
        p.update(tick)
        p.draw(screen, tick)

    draw_panel(screen, 120, 90, WIDTH - 240, 560, (10, 12, 24), 190, 24)

    pulse = int(math.sin(tick * 0.04) * 6)
    ring  = pygame.Surface((240, 240), pygame.SRCALPHA)
    ra    = int(60 + math.sin(tick * 0.04) * 30)
    pygame.draw.circle(ring, (255, 220, 80, ra), (120, 120), 118 + pulse, 1)
    screen.blit(ring, ring.get_rect(center=(WIDTH // 2, 210)))
    screen.blit(logo, logo.get_rect(center=(WIDTH // 2, 210)))

    div = pygame.Surface((300, 1), pygame.SRCALPHA)
    div.fill((255, 220, 80, 40))
    screen.blit(div, div.get_rect(center=(WIDTH // 2, 340)))

    title = label_font.render("GARUDA", True, YELLOW)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 362)))

    sub = small_font.render("Detektif Hoaks Indonesia", True, (200, 190, 170))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 392)))

    play_btn.draw(screen)
    setting_btn.draw(screen)
    exit_btn.draw(screen)

    ver = small_font.render("v1.0  ·  Garuda Studio", True, (55, 55, 55))
    screen.blit(ver, ver.get_rect(midright=(WIDTH - 22, HEIGHT - 18)))

    pygame.display.flip()

pygame.quit()
sys.exit()
