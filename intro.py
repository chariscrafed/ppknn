import os
import pygame
import sys
import math

from setting import *
from assets import load_scaled, draw_overlay, make_circle_crop

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def asset_path(*parts):
    return os.path.join(PROJECT_ROOT, "asset", *parts)


class IntroScene:

    def __init__(self):
        self.bg      = load_scaled(asset_path("kantor.jpeg"), WIDTH, HEIGHT)
        logo_raw     = load_scaled(asset_path("logo game.jpeg"), 120, 120)
        self.logo    = make_circle_crop(logo_raw, 120)
        self.f_big   = pygame.font.SysFont("Georgia", 54, bold=True)
        self.f_med   = pygame.font.SysFont("Georgia", 21)
        self.f_small = pygame.font.SysFont("Georgia", 15)

    def run(self, screen):
        clock = pygame.time.Clock()
        tick  = 0
        lines = [
            "Di era informasi, kebenaran mudah diputar balik.",
            "Hoaks menyebar lebih cepat dari fakta.",
            "Sebagai Detektif Garuda — selidiki, analisis,",
            "dan ungkap kebohongan sebelum terlambat.",
        ]

        while True:
            clock.tick(FPS)
            tick += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    if tick > 30:
                        return

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 185)

            a    = min(255, tick * 6)
            logo = self.logo.copy()
            logo.set_alpha(a)
            screen.blit(logo, logo.get_rect(center=(WIDTH // 2, 172)))

            t1 = self.f_big.render("GARUDA", True, YELLOW)
            t1.set_alpha(a)
            t2 = self.f_big.render("DETEKTIF HOAKS", True, WHITE)
            t2.set_alpha(a)
            screen.blit(t1, t1.get_rect(center=(WIDTH // 2, 268)))
            screen.blit(t2, t2.get_rect(center=(WIDTH // 2, 332)))

            lw = max(0, min(400, (tick - 20) * 12))
            if lw > 0:
                pygame.draw.line(
                    screen, (80, 80, 80),
                    (WIDTH // 2 - lw // 2, 366),
                    (WIDTH // 2 + lw // 2, 366),
                    1,
                )

            for i, line in enumerate(lines):
                fade = max(0, min(255, (tick - 55 - i * 22) * 9))
                lt   = self.f_med.render(line, True, (195, 195, 195))
                lt.set_alpha(fade)
                screen.blit(lt, lt.get_rect(center=(WIDTH // 2, 394 + i * 30)))

            blink = int(math.sin(tick * 0.09) * 70 + 120)
            sk    = self.f_small.render("Klik atau tekan tombol untuk mulai", True, (blink, blink, blink))
            screen.blit(sk, sk.get_rect(center=(WIDTH // 2, HEIGHT - 38)))

            pygame.display.flip()
