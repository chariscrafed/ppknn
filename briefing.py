import pygame
import sys
from setting import *
from assets import load_scaled, draw_overlay, draw_panel, draw_text_shadow, draw_next_button, draw_back_button

PCOL = {
    "wa":   (37, 211, 102),
    "ig":   (193,  53, 132),
    "hp":   ( 80, 160, 240),
    "uang": (255, 200,  50),
}


class BriefingScene:

    def __init__(self, case, idx):
        self.case = case
        self.idx  = idx
        self.pc   = PCOL.get(case["platform"], (120, 120, 140))

        self.ft = pygame.font.SysFont("Georgia", 28, bold=True)
        self.fb = pygame.font.SysFont("Georgia", 12, bold=True)
        self.f  = pygame.font.SysFont("Georgia", 18)
        self.fs = pygame.font.SysFont("Georgia", 13)

        self.bg      = load_scaled("asset/kantor.jpeg", WIDTH, HEIGHT)
        self.preview = load_scaled(case["preview_asset"], 330, 430)

        self.next_rect = pygame.Rect(0, 0, 224, 52)
        self.next_rect.center = (WIDTH // 2, 636)
        self.back_rect = pygame.Rect(54, 628, 126, 40)

    def run(self, screen):
        from mission import MissionScene
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_rect.collidepoint(mx, my):
                        return MissionScene(self.case, self.idx).run(screen)
                    if self.back_rect.collidepoint(mx, my):
                        return None

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 145)

            PW, PH = 980, 462
            PX = (WIDTH - PW) // 2
            PY = 110
            draw_panel(screen, PX, PY, PW, PH, (7, 9, 20), 235, 18)
            pygame.draw.rect(screen, self.pc, pygame.Rect(PX, PY, 6, PH), border_radius=18)

            L = PX + 26
            screen.blit(self.preview, (L, PY + 16))
            pygame.draw.rect(screen, (38, 38, 58),
                             pygame.Rect(L, PY + 16, 330, 430), border_radius=12, width=1)

            R  = L + 330 + 26
            RW = PX + PW - R - 18

            draw_text_shadow(screen, self.case["title"], self.ft, YELLOW, (R, PY + 18), shadow_offset=3)

            br = pygame.Rect(R, PY + 60, 160, 28)
            pygame.draw.rect(screen, self.pc, br, border_radius=8)
            badge = self.fb.render(self.case["platform_label"].upper(), True, WHITE)
            screen.blit(badge, badge.get_rect(center=br.center))

            pygame.draw.line(screen, (48, 48, 70), (R, PY + 100), (R + RW, PY + 100), 1)

            def wrap_lines(text, font, max_w, max_lines=3):
                words     = text.split()
                out, row  = [], ""
                for w in words:
                    test = row + w + " "
                    if font.size(test)[0] > max_w:
                        out.append(row.rstrip())
                        row = w + " "
                        if len(out) >= max_lines:
                            break
                    else:
                        row = test
                if row.rstrip() and len(out) < max_lines:
                    out.append(row.rstrip())
                return out

            y_cursor = PY + 114
            LINE_H   = 22
            PARA_GAP = 10
            for para in self.case["teaser"]:
                wrapped = wrap_lines(para, self.f, RW, max_lines=3)
                for ln in wrapped:
                    if y_cursor > PY + PH - 90:
                        break
                    screen.blit(self.f.render(ln, True, (235, 235, 238)), (R, y_cursor))
                    y_cursor += LINE_H
                y_cursor += PARA_GAP

            pygame.draw.line(screen, (48, 48, 70), (R, PY + 340), (R + RW, PY + 340), 1)

            screen.blit(self.fs.render("PETUNJUK INVESTIGASI", True, (255, 220, 80)), (R, PY + 350))

            words                  = self.case["hint"].split()
            line_str, lines_out    = "", []
            for w in words:
                test = line_str + w + " "
                if self.f.size(test)[0] > RW:
                    lines_out.append(line_str.strip())
                    line_str = w + " "
                else:
                    line_str = test
            lines_out.append(line_str.strip())
            for i, ln in enumerate(lines_out[:3]):
                screen.blit(self.fs.render(ln, True, (180, 182, 190)), (R, PY + 370 + i * 20))

            prog = self.fs.render(f"Kasus {self.idx + 1} dari 4", True, (98, 98, 112))
            screen.blit(prog, prog.get_rect(midright=(PX + PW - 18, PY + PH - 16)))

            draw_next_button(screen, self.next_rect,
                             hovered=self.next_rect.collidepoint(mx, my),
                             label="Mulai Investigasi  →")
            draw_back_button(screen, self.back_rect,
                             hovered=self.back_rect.collidepoint(mx, my))

            pygame.display.flip()
