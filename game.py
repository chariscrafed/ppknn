import pygame
import sys

from setting import *
from assets import load_scaled, draw_overlay, draw_panel
from briefing import BriefingScene
from score import ScoreScene


class GameScene:

    def __init__(self):
        self.bg         = load_scaled("asset/kantor.jpeg", WIDTH, HEIGHT)
        self.font_title = pygame.font.SysFont("Georgia", 36, bold=True)
        self.font       = pygame.font.SysFont("Georgia", 18)
        self.font_small = pygame.font.SysFont("Georgia", 13)
        self.font_case  = pygame.font.SysFont("Georgia", 24, bold=True)

        self.cases = [
            {
                "title": "Video Viral: Siswa Dipukuli Guru",
                "platform": "wa",
                "platform_label": "WhatsApp",
                "preview_asset": "asset/wa.jpeg",
                "teaser": [
                    "Sebuah video pendek yang memperlihatkan dugaan kekerasan "
                    "terhadap seorang siswa oleh gurunya beredar luas di grup "
                    "WhatsApp sekolah dan masyarakat. Video tersebut menarik "
                    "perhatian banyak orang dan memicu berbagai reaksi, mulai "
                    "dari kemarahan hingga tuntutan agar pihak sekolah segera "
                    "memberikan penjelasan.",
                    "Bersamaan dengan video tersebut, muncul narasi yang menyebutkan "
                    "bahwa seorang guru telah menghajar siswanya hingga mengalami "
                    "luka berat. Namun, informasi yang beredar belum disertai "
                    "kronologi lengkap, waktu kejadian, lokasi yang jelas, maupun "
                    "bukti yang dapat memastikan kebenaran seluruh tuduhan tersebut.",
                    "Video pertama kali dibagikan oleh akun anonim yang tidak "
                    "mencantumkan sumber asli. Banyak pengguna langsung memberikan "
                    "komentar negatif dan menyebarkan video tersebut tanpa "
                    "memeriksa konteks kejadian.",
                ],
                "hint": (
                    "Periksa sumber asli video, kronologi kejadian, tanggal dan "
                    "lokasi perekaman, serta klarifikasi dari pihak sekolah atau "
                    "lembaga berwenang. Utamakan fakta sebelum menyebarkan informasi."
                ),
                "has_video": False,
                "sila": 1,
                "sila_nama": "Ketuhanan Yang Maha Esa",
                "sila_pesan": (
                    "Landasan Pancasila: Sila Pertama — Ketuhanan Yang Maha Esa.\n\n"
                    "Nilai yang diterapkan:\n"
                    "1. Kejujuran dalam menyampaikan informasi.\n"
                    "2. Tanggung jawab moral atas setiap perkataan dan tindakan.\n"
                    "3. Tidak menyebarkan tuduhan tanpa bukti yang dapat dipertanggungjawabkan.\n\n"
                    "Pesan moral:\n"
                    "Ketika menerima video yang memicu emosi, jangan terburu-buru menghakimi. "
                    "Periksa fakta dan konteks terlebih dahulu."
                ),
            },
            {
                "title": "Vaksin Membahayakan Kesehatan",
                "platform": "ig",
                "platform_label": "Instagram",
                "preview_asset": "asset/ig.jpeg",
                "teaser": [
                    "Sebuah unggahan Instagram dengan judul 'Bahaya Vaksin' menjadi viral "
                    "setelah dibagikan oleh akun yang mengaku sebagai sumber informasi kesehatan. "
                    "Unggahan tersebut mengklaim vaksin menyebabkan berbagai penyakit serius "
                    "tanpa menyertakan sumber ilmiah yang jelas.",
                    "Pembuat unggahan menggunakan kalimat provokatif dan kutipan data "
                    "tanpa referensi penelitian. Efek samping vaksin disampaikan tanpa "
                    "menjelaskan konteks atau bukti ilmiah.",
                    "Akibatnya, sebagian masyarakat mulai meragukan keamanan vaksin "
                    "dan berpotensi mengabaikan saran tenaga kesehatan yang kompeten.",
                ],
                "hint": (
                    "Periksa klaim melalui Kementerian Kesehatan RI, BPOM, atau WHO. "
                    "Pastikan data berasal dari penelitian yang dapat ditelusuri."
                ),
                "has_video": False,
                "sila": 2,
                "sila_nama": "Kemanusiaan yang Adil dan Beradab",
                "sila_pesan": (
                    "Landasan Pancasila: Sila Kedua — Kemanusiaan yang Adil dan Beradab.\n\n"
                    "Nilai yang diterapkan:\n"
                    "1. Menghargai hak setiap orang untuk memperoleh informasi kesehatan yang benar.\n"
                    "2. Bersikap adil dengan menilai informasi berdasarkan bukti, bukan prasangka.\n\n"
                    "Pesan moral:\n"
                    "Informasi kesehatan harus diperiksa dengan cermat sebelum dibagikan. "
                    "Setiap orang berhak mendapatkan informasi yang akurat."
                ),
            },
            {
                "title": "Prediksi Gempa Akan Terjadi Malam Ini",
                "platform": "hp",
                "platform_label": "Handphone",
                "preview_asset": "asset/gempa.jpeg",
                "teaser": [
                    "Sebuah pesan berantai menyatakan bahwa gempa besar akan terjadi malam ini "
                    "di wilayah tertentu. Pesan tersebut disertai foto kerusakan gempa tanpa "
                    "sumber yang jelas maupun tanggal kejadian sebenarnya.",
                    "Pesan menggunakan kalimat menakutkan dan imbauan untuk segera menyebarkan "
                    "kepada keluarga. Banyak pengguna meneruskan tanpa memeriksa kebenaran informasinya.",
                    "Akibatnya masyarakat menjadi panik, padahal informasi kebencanaan harus "
                    "diperoleh dari sumber resmi seperti BMKG.",
                ],
                "hint": (
                    "Periksa informasi melalui BMKG dan BNPB. "
                    "Jangan langsung meneruskan pesan berantai yang menimbulkan kepanikan."
                ),
                "has_video": False,
                "sila": 3,
                "sila_nama": "Persatuan Indonesia",
                "sila_pesan": (
                    "Landasan Pancasila: Sila Ketiga — Persatuan Indonesia.\n\n"
                    "Nilai yang diterapkan:\n"
                    "1. Menjaga ketenangan dan keharmonisan masyarakat.\n"
                    "2. Menghindari tindakan yang menimbulkan kepanikan dan perpecahan.\n\n"
                    "Pesan moral:\n"
                    "Ketika menerima informasi bencana, periksa sumber terlebih dahulu "
                    "dan bantu orang lain mendapatkan petunjuk keselamatan yang benar."
                ),
            },
            {
                "title": "Uang Palsu Beredar di Pasar Tradisional",
                "platform": "uang",
                "platform_label": "Uang",
                "preview_asset": "asset/uang.jpeg",
                "teaser": [
                    "Foto uang Rupiah yang diduga palsu beredar di media sosial. "
                    "Unggahan tersebut menyatakan uang palsu telah beredar dalam jumlah besar "
                    "di pasar tradisional sehingga membuat pedagang dan pembeli khawatir.",
                    "Sebuah akun lokal menuduh pihak tertentu bertanggung jawab, namun "
                    "tidak menyertakan hasil pemeriksaan resmi atau keterangan dari lembaga berwenang.",
                    "Jika disebarkan tanpa pemeriksaan, masyarakat dapat kehilangan kepercayaan "
                    "dan pihak yang tidak bersalah berpotensi menjadi sasaran tuduhan.",
                ],
                "hint": (
                    "Periksa informasi melalui Bank Indonesia atau kepolisian. "
                    "Hindari menuduh pihak tertentu tanpa bukti yang dapat dipertanggungjawabkan."
                ),
                "has_video": False,
                "sila": 4,
                "sila_nama": "Kerakyatan yang Dipimpin oleh Hikmat Kebijaksanaan dalam Permusyawaratan/Perwakilan",
                "sila_pesan": (
                    "Landasan Pancasila: Sila Keempat — Kerakyatan yang Dipimpin oleh Hikmat "
                    "Kebijaksanaan dalam Permusyawaratan/Perwakilan.\n\n"
                    "Nilai yang diterapkan:\n"
                    "1. Mengutamakan pemikiran yang rasional dan bijaksana.\n"
                    "2. Memeriksa bukti sebelum mengambil keputusan.\n\n"
                    "Pesan moral:\n"
                    "Setiap keputusan harus diambil dengan pertimbangan matang, bukan karena emosi. "
                    "Jangan mudah menuduh seseorang tanpa dasar yang jelas."
                ),
            },
        ]

        self.results   = []
        self.back_rect = pygame.Rect(30, 650, 170, 46)
        self.play_rect = pygame.Rect(WIDTH // 2 - 120, 650, 240, 46)

    def _draw_case(self, screen, case, rect, idx, hovered):
        color = (35, 42, 54) if not hovered else (46, 58, 74)
        pygame.draw.rect(screen, color, rect, border_radius=16)
        pygame.draw.rect(screen, (255, 220, 80), rect, border_radius=16, width=1)

        tag = self.font_small.render(f"Kasus {idx + 1}  ·  {case['platform_label'].upper()}", True, (255, 220, 80))
        screen.blit(tag, (rect.x + 18, rect.y + 14))

        title = self.font_case.render(case["title"], True, WHITE)
        screen.blit(title, (rect.x + 18, rect.y + 40))

        max_chars = 95
        hint_text = case["hint"]
        if len(hint_text) > max_chars:
            cut       = hint_text[:max_chars].rsplit(" ", 1)[0]
            hint_text = cut + "..."
        hint = self.font_small.render(hint_text, True, (170, 172, 185))
        screen.blit(hint, (rect.x + 18, rect.y + 74))

    def run(self, screen):
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_rect.collidepoint(mx, my):
                        return
                    if self.play_rect.collidepoint(mx, my):
                        if self.results:
                            ScoreScene(self.results).run(screen)
                        return
                    for idx, case in enumerate(self.cases):
                        rect = pygame.Rect(120, 130 + idx * 120, WIDTH - 240, 98)
                        if rect.collidepoint(mx, my):
                            result = BriefingScene(case, idx).run(screen)
                            if result is not None and isinstance(result, dict):
                                self.results.append(result)
                            return

            screen.blit(self.bg, (0, 0))
            draw_overlay(screen, 110)
            draw_panel(screen, 90, 70, WIDTH - 180, 560, (8, 10, 22), 220, 18)

            title = self.font_title.render("DETEKTIF HOAKS — PILIH KASUS", True, YELLOW)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

            for idx, case in enumerate(self.cases):
                rect = pygame.Rect(120, 130 + idx * 120, WIDTH - 240, 98)
                self._draw_case(screen, case, rect, idx, rect.collidepoint(mx, my))

            back_hover = self.back_rect.collidepoint(mx, my)
            play_hover = self.play_rect.collidepoint(mx, my)

            pygame.draw.rect(screen, (70, 70, 75) if back_hover else (50, 50, 60), self.back_rect, border_radius=12)
            pygame.draw.rect(screen, (60, 120, 255) if play_hover else (37, 99, 235), self.play_rect, border_radius=12)

            screen.blit(self.font.render("KEMBALI",    True, WHITE),
                        self.font.render("KEMBALI",    True, WHITE).get_rect(center=self.back_rect.center))
            screen.blit(self.font.render("LIHAT HASIL", True, WHITE),
                        self.font.render("LIHAT HASIL", True, WHITE).get_rect(center=self.play_rect.center))

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    GameScene().run(screen)
    pygame.quit()
    sys.exit()
