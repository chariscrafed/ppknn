import pygame
import sys
import math

from setting import *
from assets import load_scaled, draw_overlay, draw_panel, draw_next_button

GOLD = (255, 215, 70)
DARK = (8, 10, 22)

SILA1_NAMA  = "Ketuhanan Yang Maha Esa"
SILA1_PESAN = (
    "Sila Pertama adalah landasan utama Pancasila. Kejujuran, hati nurani, "
    "dan tanggung jawab moral harus diutamakan dalam setiap tindakan, "
    "termasuk dalam menerima dan menyebarkan informasi."
)


class ResultScene:

    def __init__(self, correct, case_title, sila=1, sila_nama="", sila_pesan=""):
        self.correct    = correct
        self.case_title = case_title
        self.sila       = sila
        self.sila_nama  = sila_nama
        self.sila_pesan = sila_pesan
        self.tick       = 0

        self.f_hero   = pygame.font.SysFont("Georgia", 34, bold=True)
        self.f_sub    = pygame.font.SysFont("Georgia", 17)
        self.f_sila   = pygame.font.SysFont("Georgia", 16, bold=True)
        self.f_num    = pygame.font.SysFont("Georgia", 30, bold=True)
        self.f_body   = pygame.font.SysFont("Georgia", 15)
        self.f_label  = pygame.font.SysFont("Georgia", 12, bold=True)
        self.f_header = pygame.font.SysFont("Georgia", 13, bold=True)

        self.sertif    = load_scaled("asset/sertif2.jpeg", 340, 228)
        self.bg        = load_scaled("asset/kantor.jpeg", WIDTH, HEIGHT)
        self.next_rect = pygame.Rect(0, 0, 200, 46)

    def _wrap(self, text, font, max_w):
        words    = text.split()
        out, row = [], ""
        for w in words:
            test = row + w + " "
            if font.size(test)[0] > max_w:
                if row:
                    out.append(row.rstrip())
                row = w + " "
            else:
                row = test
        if row.rstrip():
            out.append(row.rstrip())
        return out

    def _div(self, screen, x, y, w, alpha=60):
        s = pygame.Surface((w, 1), pygame.SRCALPHA)
        s.fill((*GOLD, alpha))
        screen.blit(s, (x, y))

    def _render_lines(self, screen, lines, font, color, x, y, line_h, bottom, fade=255):
        for ln in lines:
            if y + line_h > bottom:
                break
            surf = font.render(ln, True, color)
            surf.set_alpha(fade)
            screen.blit(surf, (x, y))
            y += line_h
        return y

    def _sila_badge_row(self, screen, x, y, num, nama, iw, bottom):
        badge = pygame.Rect(x, y, 48, 48)
        pygame.draw.rect(screen, (20, 24, 42), badge, border_radius=10)
        pygame.draw.rect(screen, (*GOLD, 110), badge, border_radius=10, width=1)
        screen.blit(
            self.f_num.render(str(num), True, GOLD),
            self.f_num.render(str(num), True, GOLD).get_rect(center=badge.center)
        )
        tx = x + 58
        tw = iw - 58
        screen.blit(self.f_label.render(f"SILA KE-{num}", True, (*GOLD, 160)), (tx, y + 4))
        yn = y + 22
        for ln in self._wrap(nama, self.f_sila, tw):
            if yn + 18 > bottom:
                break
            screen.blit(self.f_sila.render(ln, True, GOLD), (tx, yn))
            yn += 20
        return max(y + 54, yn + 4)

    def run(self, screen):
        clock = pygame.time.Clock()

        PW = WIDTH - 80
        PH = HEIGHT - 80
        PX = 40
        PY = 40

        LW = 380
        RX = PX + LW + 16
        RW = PW - LW - 16

        self.next_rect.center = (WIDTH // 2, PY + PH + 24)

        while True:
            clock.tick(FPS)
            self.tick += 1
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_rect.collidepoint(mx, my):
                        return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 182)

            col     = GREEN if self.correct else RED
            accent  = GOLD  if self.correct else RED
            pulse_a = int(50 + math.sin(self.tick * 0.07) * 28)
            shimmer = int(188 + math.sin(self.tick * 0.05) * 36)
            fade    = min(255, max(0, (self.tick - 10) * 14))
            CX_L    = PX + LW // 2

            draw_panel(screen, PX, PY, LW, PH, DARK, 236, 18)

            brd = pygame.Surface((LW, PH), pygame.SRCALPHA)
            pygame.draw.rect(brd, (*accent, pulse_a), brd.get_rect(), border_radius=18, width=2)
            screen.blit(brd, (PX, PY))

            tbar = pygame.Surface((LW, 5), pygame.SRCALPHA)
            pygame.draw.rect(tbar, (*accent, 220), tbar.get_rect(), border_radius=3)
            screen.blit(tbar, (PX, PY))

            screen.blit(self.sertif, self.sertif.get_rect(center=(CX_L, PY + 22 + 114)))

            d1 = PY + 22 + 228 + 10
            self._div(screen, PX + 20, d1, LW - 40)

            hero_col = (shimmer, 218, 55) if self.correct else (shimmer, 55, 55)
            hs = self.f_hero.render("✓  BENAR!" if self.correct else "✗  SALAH!", True, hero_col)
            screen.blit(hs, hs.get_rect(center=(CX_L, d1 + 30)))

            sub_s = self.f_sub.render(
                "Hoaks berhasil diungkap!" if self.correct else "Terjebak informasi palsu.",
                True, (208, 214, 226))
            screen.blit(sub_s, sub_s.get_rect(center=(CX_L, d1 + 64)))

            d2 = d1 + 84
            self._div(screen, PX + 20, d2, LW - 40)

            for j, ln in enumerate(self._wrap(self.case_title, self.f_header, LW - 48)[:2]):
                s = self.f_header.render(ln, True, (130, 138, 160))
                screen.blit(s, s.get_rect(center=(CX_L, d2 + 14 + j * 18)))

            vy = d2 + 14 + 2 * 18 + 8
            vbg = pygame.Surface((LW - 56, 38), pygame.SRCALPHA)
            pygame.draw.rect(vbg, (*col, 30), vbg.get_rect(), border_radius=10)
            pygame.draw.rect(vbg, (*col, 90), vbg.get_rect(), border_radius=10, width=1)
            screen.blit(vbg, (PX + 28, vy))
            vt = self.f_sub.render(
                "✓  Jawaban Benar" if self.correct else "✗  Jawaban Salah", True, col)
            screen.blit(vt, vt.get_rect(center=(CX_L, vy + 19)))

            tip = self.f_label.render("💡 Selalu verifikasi sebelum menyebarkan", True, (70, 75, 95))
            screen.blit(tip, tip.get_rect(center=(CX_L, PY + PH - 16)))

            draw_panel(screen, RX, PY, RW, PH, DARK, 236, 18)

            gbar = pygame.Surface((RW, 5), pygame.SRCALPHA)
            pygame.draw.rect(gbar, (*GOLD, 210), gbar.get_rect(), border_radius=3)
            screen.blit(gbar, (RX, PY))

            IX = RX + 18
            IW = RW - 36
            YC = PY + 16
            BG = PY + PH - 16

            screen.blit(self.f_header.render("LANDASAN PANCASILA", True, (108, 114, 142)), (IX, YC))
            YC += 20
            self._div(screen, IX, YC, IW, 45)
            YC += 12

            sila1_lines = self._wrap(SILA1_PESAN, self.f_body, IW)
            YC = self._sila_badge_row(screen, IX, YC, 1, SILA1_NAMA, IW, BG - 60)
            YC = self._render_lines(screen, sila1_lines, self.f_body,
                                    (215, 218, 230), IX, YC, 20, BG - 60, fade)

            YC += 10
            self._div(screen, IX, YC, IW, 38)
            YC += 12

            if self.sila != 1 and YC + 60 < BG:
                sila_n_pesan = ""
                capturing    = False
                for raw in self.sila_pesan.split("\n"):
                    if raw.strip().startswith("Pesan moral"):
                        capturing = True
                        break
                    if raw.strip() and not raw.strip().startswith("Landasan") \
                            and not raw.strip().startswith("Nilai"):
                        sila_n_pesan += raw.strip() + " "

                YC = self._sila_badge_row(screen, IX, YC, self.sila, self.sila_nama, IW, BG - 60)
                sila_n_lines = self._wrap(sila_n_pesan.strip(), self.f_body, IW)
                YC = self._render_lines(screen, sila_n_lines, self.f_body,
                                        (215, 218, 230), IX, YC, 20, BG - 60, fade)
                YC += 10
                self._div(screen, IX, YC, IW, 38)
                YC += 12

            if YC + 40 < BG:
                screen.blit(self.f_header.render("PESAN MORAL", True, GOLD), (IX, YC))
                YC += 20

                pesan_moral = ""
                capturing   = False
                for raw in self.sila_pesan.split("\n"):
                    if raw.strip().startswith("Pesan moral"):
                        capturing = True
                        continue
                    if capturing and raw.strip():
                        pesan_moral += raw.strip() + " "

                moral_lines = self._wrap(pesan_moral.strip(), self.f_body, IW)
                self._render_lines(screen, moral_lines, self.f_body,
                                   (222, 225, 235), IX, YC, 20, BG, fade)

            draw_next_button(screen, self.next_rect,
                             hovered=self.next_rect.collidepoint(mx, my),
                             label="Lanjut  →")

            pygame.display.flip()
