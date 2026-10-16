import pygame
import sys
import math

from setting import *
from assets import load_scaled, draw_overlay, draw_panel, draw_next_button

GOLD = (255, 215, 70)
DARK = (8, 10, 22)

RANK_DATA = {
    "S": {"color": GOLD,          "label": "Detektif Legendaris", "desc": "Sempurna! Tidak ada hoaks yang lolos."},
    "A": {"color": GREEN,         "label": "Detektif Andal",      "desc": "Hebat! Kamu hampir sempurna."},
    "B": {"color": (80, 180, 255), "label": "Detektif Pemula",    "desc": "Lumayan! Terus tingkatkan."},
    "C": {"color": RED,           "label": "Perlu Belajar Lagi",  "desc": "Jangan menyerah, terus berlatih!"},
}

class ScoreScene:

    def __init__(self, results):
        self.results   = results
        self.tick      = 0

        total = len(results)
        benar = sum(1 for r in results if r["correct"])
        self.score_pct = int(benar / total * 100) if total else 0
        self.benar     = benar

        if self.score_pct == 100:
            rk = "S"
        elif self.score_pct >= 75:
            rk = "A"
        elif self.score_pct >= 50:
            rk = "B"
        else:
            rk = "C"

        self.rank_key  = rk
        self.rank_info = RANK_DATA[rk]

        self.f_title = pygame.font.SysFont("Georgia", 30, bold=True)
        self.f_rank  = pygame.font.SysFont("Georgia", 62, bold=True)
        self.f_big   = pygame.font.SysFont("Georgia", 26, bold=True)
        self.f_med   = pygame.font.SysFont("Georgia", 16, bold=True)
        self.f_body  = pygame.font.SysFont("Georgia", 14)
        self.f_small = pygame.font.SysFont("Georgia", 13)
        self.f_label = pygame.font.SysFont("Georgia", 11, bold=True)

        self.sertif    = load_scaled("asset/sertif2.jpeg", 200, 134)
        self.bg        = load_scaled("asset/kantor.jpeg", WIDTH, HEIGHT)
        self.next_rect = pygame.Rect(0, 0, 210, 44)

    def _div(self, screen, x, y, w):
        s = pygame.Surface((w, 1), pygame.SRCALPHA)
        s.fill((255, 215, 70, 50))
        screen.blit(s, (x, y))

    def run(self, screen):
        clock = pygame.time.Clock()

        PW = 900
        PX = (WIDTH - PW) // 2

        while True:
            clock.tick(FPS)
            self.tick += 1
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_rect.collidepoint(mx, my):
                        return

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 178)

            rank_col = self.rank_info["color"]
            pulse    = int(45 + math.sin(self.tick * 0.06) * 22)

            N        = len(self.results)
            ROW_H    = 48
            PH       = 56 + 16 + 154 + 16 + 32 + (N * ROW_H) + 20 + 56
            PH       = max(PH, 580)
            PY       = max(10, (HEIGHT - PH) // 2 - 12)
            CX       = WIDTH // 2

            draw_panel(screen, PX, PY, PW, PH, DARK, 234, 20)

            bar = pygame.Surface((PW, 5), pygame.SRCALPHA)
            pygame.draw.rect(bar, (*GOLD, 210), bar.get_rect(), border_radius=3)
            screen.blit(bar, (PX, PY))

            YC    = PY + 16
            title = self.f_title.render("HASIL INVESTIGASI", True, GOLD)
            shad  = self.f_title.render("HASIL INVESTIGASI", True, (0, 0, 0))
            shad.set_alpha(70)
            screen.blit(shad, title.get_rect(center=(CX + 2, YC + 2 + 12)))
            screen.blit(title, title.get_rect(center=(CX, YC + 12)))

            YC += 42
            self._div(screen, PX + 24, YC, PW - 48)
            YC += 16

            SERT_X = PX + 32

            screen.blit(self.sertif, (SERT_X, YC))
            sbrd = pygame.Surface((200, 134), pygame.SRCALPHA)
            pygame.draw.rect(sbrd, (*GOLD, 55), sbrd.get_rect(), border_radius=10, width=1)
            screen.blit(sbrd, (SERT_X, YC))

            INFO_X = SERT_X + 200 + 32
            INFO_W = PW - (INFO_X - PX) - 32

            rank_surf = self.f_rank.render(self.rank_key, True, rank_col)
            rw, rh    = rank_surf.get_size()

            glow_w = rw + 18
            glow_h = rh + 10
            if INFO_X + glow_w > PX + PW - 32:
                glow_w = (PX + PW - 32) - INFO_X

            glow = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*rank_col, pulse), glow.get_rect(), border_radius=12)
            screen.blit(glow, (INFO_X, YC + 10))
            screen.blit(rank_surf, (INFO_X + 9, YC + 15))

            pct_surf = self.f_big.render(f"{self.score_pct}%", True, WHITE)
            screen.blit(pct_surf, (INFO_X + glow_w + 18, YC + 26))

            lbl_surf = self.f_med.render(self.rank_info["label"], True, rank_col)
            screen.blit(lbl_surf, (INFO_X, YC + 76))

            desc_surf = self.f_body.render(self.rank_info["desc"], True, (185, 190, 205))
            screen.blit(desc_surf, (INFO_X, YC + 98))

            det = self.f_small.render(
                f"{self.benar} dari {len(self.results)} kasus dijawab benar", True, (165, 170, 190))
            screen.blit(det, (INFO_X, YC + 120))

            YC += 154
            self._div(screen, PX + 24, YC, PW - 48)
            YC += 12

            hdr_bg = pygame.Surface((PW - 48, 24), pygame.SRCALPHA)
            pygame.draw.rect(hdr_bg, (255, 215, 70, 16), hdr_bg.get_rect(), border_radius=6)
            screen.blit(hdr_bg, (PX + 24, YC))
            screen.blit(self.f_label.render("RINCIAN KASUS", True, GOLD), (PX + 36, YC + 6))
            YC += 32

            for i, r in enumerate(self.results):
                y     = YC + i * ROW_H
                col   = GREEN if r["correct"] else RED
                is_ok = r["correct"]

                rbg = pygame.Surface((PW - 48, ROW_H - 4), pygame.SRCALPHA)
                pygame.draw.rect(rbg, (14, 18, 32, 210), rbg.get_rect(), border_radius=8)
                if is_ok:
                    pygame.draw.rect(rbg, (*GREEN, 18), rbg.get_rect(), border_radius=8)
                screen.blit(rbg, (PX + 24, y))

                pygame.draw.rect(screen, (*col, 190),
                                 pygame.Rect(PX + 24, y, 4, ROW_H - 4), border_radius=2)

                mark = self.f_body.render("✓" if is_ok else "✗", True, col)
                screen.blit(mark, (PX + 36, y + 8))

                title_s = self.f_body.render(r["title"], True, (235, 240, 248))
                screen.blit(title_s, (PX + 56, y + 6))

                ans = f"Jawaban: {r['selected']}   ·   Benar: {r['answer']}"
                ans_s = self.f_small.render(ans, True, (140, 220, 140) if is_ok else (235, 130, 130))
                screen.blit(ans_s, (PX + 56, y + 28))

            YC += N * ROW_H + 16
            self._div(screen, PX + 24, YC, PW - 48)
            YC += 18

            self.next_rect.center = (CX, YC + 20)
            draw_next_button(screen, self.next_rect,
                             hovered=self.next_rect.collidepoint(mx, my),
                             label="Kembali ke Menu  →")

            pygame.display.flip()
