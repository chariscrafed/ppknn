import pygame
import sys
import numpy as np

from setting import *
from assets import load_scaled, draw_overlay, draw_panel


def generate_click():
    """Generate click sound effect using sine wave."""
    sr = 44100
    dur = 0.06
    t = np.linspace(0, dur, int(sr * dur), False)
    wav = np.sin(2 * np.pi * 800 * t) * np.exp(-t * 60)
    wav = (wav * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((wav, wav)))


class SettingsScene:
    """Settings menu for game configuration."""

    def __init__(self):
        self.music_vol = 80
        self.sound_vol = 70
        self.music_on = True
        self.fullscreen = False

        self.font_title = pygame.font.SysFont("Georgia", 38, bold=True)
        self.font = pygame.font.SysFont("Georgia", 20)
        self.font_small = pygame.font.SysFont("Georgia", 13)
        self.bg = load_scaled("asset/kantor.jpeg", WIDTH, HEIGHT)
        self.back_rect = pygame.Rect((WIDTH - 260) // 2, 600, 260, 54)
        self.click_sfx = generate_click()

        self.SX = 520
        self.MW_Y = 235
        self.SW_Y = 305

    def _play(self):
        """Play click sound effect."""
        self.click_sfx.set_volume(self.sound_vol / 100)
        self.click_sfx.play()

    def _slider(self, screen, x, y, val):
        """Draw volume slider."""
        pygame.draw.rect(screen, (70, 76, 90), (x, y, 220, 8), border_radius=4)
        pygame.draw.rect(screen, (37, 99, 235), (x, y, val * 2.2, 8), border_radius=4)
        pygame.draw.circle(screen, (255, 255, 255), (x + int(val * 2.2), y + 4), 9)

    def _checkbox(self, screen, x, y, state):
        """Draw checkbox with check mark if enabled."""
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 22, 22), 2, border_radius=5)
        if state:
            pygame.draw.line(screen, (50, 200, 90), (x + 3, y + 11), (x + 9, y + 17), 3)
            pygame.draw.line(screen, (50, 200, 90), (x + 9, y + 17), (x + 19, y + 5), 3)

    def run(self, screen):
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_rect.collidepoint(mx, my):
                        self._play(); return
                    if self.SX <= mx <= self.SX + 220 and self.MW_Y - 10 <= my <= self.MW_Y + 20:
                        self.music_vol = max(0, min(100, (mx - self.SX) / 2.2))
                        pygame.mixer.music.set_volume(self.music_vol / 100)
                        self._play()
                    if self.SX <= mx <= self.SX + 220 and self.SW_Y - 10 <= my <= self.SW_Y + 20:
                        self.sound_vol = max(0, min(100, (mx - self.SX) / 2.2))
                        self._play()
                    if self.SX <= mx <= self.SX + 22 and 372 <= my <= 394:
                        self.music_on = not self.music_on
                        self._play()
                        pygame.mixer.music.unpause() if self.music_on else pygame.mixer.music.pause()
                    if self.SX <= mx <= self.SX + 22 and 432 <= my <= 454:
                        self.fullscreen = not self.fullscreen
                        self._play()
                        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if self.fullscreen else 0)

                if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                    if self.MW_Y - 10 <= my <= self.MW_Y + 20:
                        self.music_vol = max(0, min(100, (mx - self.SX) / 2.2))
                        pygame.mixer.music.set_volume(self.music_vol / 100)
                    if self.SW_Y - 10 <= my <= self.SW_Y + 20:
                        self.sound_vol = max(0, min(100, (mx - self.SX) / 2.2))

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 100)
            draw_panel(screen, 220, 110, 840, 480, (8, 10, 22), 225, 20)

            title = self.font_title.render("PENGATURAN", True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))
            pygame.draw.line(screen, (55, 55, 75), (280, 180), (1000, 180), 1)

            rows = [
                ("Volume Musik", self.SX, self.MW_Y, "slider", self.music_vol),
                ("Volume Efek", self.SX, self.SW_Y, "slider", self.sound_vol),
                ("Musik", self.SX, 372, "check", self.music_on),
                ("Fullscreen", self.SX, 432, "check", self.fullscreen),
            ]

            for label, x, y, kind, val in rows:
                lbl = self.font.render(label, True, WHITE)
                screen.blit(lbl, (320, y - 5))
                if kind == "slider":
                    self._slider(screen, x, y, val)
                else:
                    self._checkbox(screen, x, y, val)

            hov = self.back_rect.collidepoint(mx, my)
            color = (60, 120, 255) if hov else BLUE
            pygame.draw.rect(screen, color, self.back_rect, border_radius=12)
            back_txt = self.font.render("KEMBALI", True, WHITE)
            screen.blit(back_txt, back_txt.get_rect(center=self.back_rect.center))

            pygame.display.flip()
