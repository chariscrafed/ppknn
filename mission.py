import pygame
import sys
from setting import *
from assets import load_scaled, draw_overlay, draw_panel, draw_text_shadow, draw_verdict_button, draw_next_button

try:
    import cv2
    import numpy as np
    CV2_OK = True
except ImportError:
    CV2_OK = False

try:
    if not CV2_OK:
        import numpy as np
    def _make_sfx(freq, dur=0.07):
        sr = 44100
        t  = np.linspace(0, dur, int(sr * dur), False)
        w  = np.sin(2 * np.pi * freq * t) * np.exp(-t * 50)
        w  = (w * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack((w, w)))
    SFX_OK = True
except Exception:
    SFX_OK = False

PLATFORM_COLORS = {
    "wa":   (37, 211, 102),
    "ig":   (193,  53, 132),
    "hp":   ( 80, 160, 240),
    "uang": (255, 200,  50),
}

PLATFORM_ASSETS = {
    "wa":   "asset/wa.jpeg",
    "ig":   "asset/ig.jpeg",
    "hp":   "asset/hp.jpeg",
    "uang": "asset/uang.jpeg",
    "gempa":"asset/gempa.jpeg",
}

VERDICTS = [
    {
        "answer": "HOAX",
        "clues": [
            "Video diambil tanpa konteks — itu adegan drama sekolah",
            "Pihak sekolah merilis klarifikasi resmi 2 jam setelah viral",
            "Guru tidak pernah melakukan tindak kekerasan nyata",
        ],
    },
    {
        "answer": "HOAX",
        "clues": [
            "Kementerian Kesehatan RI menegaskan vaksin telah diuji dan dinyatakan aman",
            "Bukti uji klinis dan publikasi ilmiah mendukung keamanan vaksin",
            "WHO mengimbau waspada terhadap disinformasi kesehatan",
        ],
    },
    {
        "answer": "HOAX",
        "clues": [
            "Tidak ada lembaga resmi yang merilis prediksi gempa ini",
            "BMKG menegaskan tidak pernah membuat pernyataan tersebut",
            "Foto yang digunakan diambil dari peristiwa gempa berbeda",
        ],
    },
    {
        "answer": "FAKTA",
        "clues": [
            "Bank Indonesia mengkonfirmasi peredaran uang palsu tersebut",
            "Foto sesuai dengan rilis resmi yang dikeluarkan pihak BI",
            "Kepolisian setempat telah menerima dan memproses laporan",
        ],
    },
]


class VideoPlayer:

    def __init__(self, path, rect):
        self.rect  = rect
        self.frame = None
        self.cap   = None
        if CV2_OK:
            try:
                self.cap = cv2.VideoCapture(path)
            except Exception:
                pass

    def update(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            if ret:
                frame      = cv2.resize(frame, (self.rect.width, self.rect.height))
                frame      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame = pygame.surfarray.make_surface(np.rot90(frame))

    def draw(self, surface):
        if self.frame is not None:
            surface.blit(self.frame, self.rect.topleft)
        else:
            pygame.draw.rect(surface, (14, 14, 22), self.rect, border_radius=8)
            f = pygame.font.SysFont("Georgia", 13)
            t = f.render("pip install opencv-python  untuk putar video", True, (60, 60, 70))
            surface.blit(t, t.get_rect(center=self.rect.center))

    def release(self):
        if self.cap:
            self.cap.release()


class MissionScene:

    def __init__(self, case, idx):
        self.case    = case
        self.idx     = idx
        self.verdict = VERDICTS[idx]
        self.pcol    = PLATFORM_COLORS.get(case["platform"], (120, 120, 140))

        self.font_title = pygame.font.SysFont("Georgia", 24, bold=True)
        self.font       = pygame.font.SysFont("Georgia", 18)
        self.font_small = pygame.font.SysFont("Georgia", 14)
        self.font_big   = pygame.font.SysFont("Georgia", 28, bold=True)
        self.font_badge = pygame.font.SysFont("Georgia", 12, bold=True)

        self.bg           = load_scaled("asset/meja.jpeg", WIDTH, HEIGHT)
        platform_asset    = PLATFORM_ASSETS.get(case["platform"], case.get("preview_asset", "asset/kantor.jpeg"))
        self.platform_img = load_scaled(platform_asset, 300, 410)

        LW, LH = 320, 450
        LX, LY = 40, 112

        if case.get("has_video"):
            video_path = case.get("video_path", "asset/video.mp4")
            self.video = VideoPlayer(video_path, pygame.Rect(LX, LY, LW, LH))
        else:
            self.video = None

        self.LX, self.LY, self.LW, self.LH = LX, LY, LW, LH

        self.btn_hoax  = pygame.Rect(WIDTH // 2 - 220, 628, 195, 52)
        self.btn_fakta = pygame.Rect(WIDTH // 2 +  25, 628, 195, 52)
        self.next_rect = pygame.Rect(0, 0, 200, 50)
        self.next_rect.center = (WIDTH // 2, 660)

        self.sfx_correct = _make_sfx(880) if SFX_OK else None
        self.sfx_wrong   = _make_sfx(220) if SFX_OK else None

        self.selected    = None
        self.show_result = False
        self.clue_idx    = 0
        self.tick        = 0

    def run(self, screen):
        from result import ResultScene
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            self.tick += 1
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.video: self.video.release()
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.video: self.video.release()
                        return None
                    if event.key == pygame.K_SPACE and not self.show_result:
                        self.clue_idx = min(self.clue_idx + 1, len(self.verdict["clues"]) - 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.show_result:
                        if self.btn_hoax.collidepoint(mx, my):
                            self.selected    = "HOAX"
                            self.show_result = True
                        elif self.btn_fakta.collidepoint(mx, my):
                            self.selected    = "FAKTA"
                            self.show_result = True
                    else:
                        if self.next_rect.collidepoint(mx, my):
                            if self.video: self.video.release()
                            correct = self.selected == self.verdict["answer"]
                            ResultScene(
                                correct,
                                self.case["title"],
                                self.case.get("sila", 1),
                                self.case.get("sila_nama", ""),
                                self.case.get("sila_pesan", ""),
                            ).run(screen)
                            return {
                                "title"   : self.case["title"],
                                "correct" : correct,
                                "answer"  : self.verdict["answer"],
                                "selected": self.selected,
                            }

            if self.video: self.video.update()

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 145)

            LX, LY, LW, LH = self.LX, self.LY, self.LW, self.LH

            draw_panel(screen, LX, LY, LW, LH, (8, 10, 22), 205, 14)
            pygame.draw.rect(screen, self.pcol, pygame.Rect(LX, LY, 4, LH), border_radius=10)

            if self.video:
                self.video.draw(screen)
                vid_lbl = self.font_small.render("▶ BARANG BUKTI — VIDEO VIRAL", True, self.pcol)
                screen.blit(vid_lbl, vid_lbl.get_rect(center=(LX + LW // 2, LY + LH + 16)))
            else:
                screen.blit(self.platform_img,
                            self.platform_img.get_rect(center=(LX + LW // 2, LY + LH // 2)))

            pygame.draw.rect(screen, (35, 35, 55),
                             pygame.Rect(LX, LY, LW, LH), border_radius=14, width=1)

            badge_r = pygame.Rect(LX + 12, LY + LH + 8, 160, 22)
            pygame.draw.rect(screen, self.pcol, badge_r, border_radius=5)
            badge_txt = self.font_badge.render(self.case["platform_label"].upper(), True, WHITE)
            screen.blit(badge_txt, badge_txt.get_rect(center=badge_r.center))

            RX = LX + LW + 32
            RW = WIDTH - RX - 40
            RH = 475
            RY = 108
            draw_panel(screen, RX, RY, RW, RH, (6, 8, 20), 218, 16)
            pygame.draw.rect(screen, self.pcol, pygame.Rect(RX, RY, 4, RH), border_radius=10)

            draw_text_shadow(screen, self.case["title"], self.font_title, YELLOW, (RX + 18, RY + 16))
            pygame.draw.line(screen, (50, 50, 72), (RX + 14, RY + 52), (RX + RW - 14, RY + 52), 1)

            screen.blit(
                self.font_small.render("▸  CATATAN INVESTIGASI", True, (90, 90, 115)),
                (RX + 18, RY + 62)
            )

            for i, clue in enumerate(self.verdict["clues"]):
                if i <= self.clue_idx:
                    fade = min(255, (self.tick - i * 28) * 14) if not self.show_result else 255
                    pygame.draw.circle(screen, self.pcol, (RX + 28, RY + 96 + i * 42 + 7), 4)
                    ct = self.font.render(clue, True, WHITE)
                    ct.set_alpha(max(0, fade))
                    screen.blit(ct, (RX + 42, RY + 90 + i * 42))

            if not self.show_result:
                draw_verdict_button(screen, self.btn_hoax,  "✗  HOAX",  RED,   self.btn_hoax.collidepoint(mx, my))
                draw_verdict_button(screen, self.btn_fakta, "✓  FAKTA", GREEN, self.btn_fakta.collidepoint(mx, my))
            else:
                correct = self.selected == self.verdict["answer"]
                col = GREEN if correct else RED
                vt  = self.font_big.render(
                    ("✓  BENAR!  " if correct else "✗  SALAH!  ") + f"Ini adalah {self.verdict['answer']}",
                    True, col
                )
                screen.blit(vt, vt.get_rect(center=(WIDTH // 2, 600)))
                draw_next_button(screen, self.next_rect,
                                 hovered=self.next_rect.collidepoint(mx, my),
                                 label="Lihat Hasil  →")

            screen.blit(
                self.font_small.render(
                    f"Kasus {self.idx + 1} dari 4  ·  {self.case['platform_label']}", True, (65, 65, 85)
                ),
                (RX + 18, RY + RH - 20)
            )

            pygame.display.flip()
