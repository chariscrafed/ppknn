import os
import pygame
from setting import WIDTH, HEIGHT, WHITE

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def asset_path(*parts):
    return os.path.join(PROJECT_ROOT, *parts)


def load_scaled(path, w, h, alpha=False):
    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()
    return pygame.transform.smoothscale(img, (w, h))


def load_cropped(path, w, h):
    img      = pygame.image.load(path).convert()
    iw, ih   = img.get_size()
    scale    = max(w / iw, h / ih)
    nw, nh   = int(iw * scale), int(ih * scale)
    img      = pygame.transform.smoothscale(img, (nw, nh))
    cx, cy   = (nw - w) // 2, (nh - h) // 2
    return img.subsurface(pygame.Rect(cx, cy, w, h)).copy()


def make_circle_crop(surf, size):
    result = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(result, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
    result.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return result


def draw_panel(surface, x, y, w, h, color=(10, 12, 28), alpha=215, radius=16):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=radius)
    surface.blit(s, (x, y))


def draw_overlay(surface, alpha=100):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, alpha))
    surface.blit(ov, (0, 0))


def draw_text_shadow(surface, text, font, color, pos, shadow_offset=2):
    shadow = font.render(text, True, (0, 0, 0))
    shadow.set_alpha(120)
    surface.blit(shadow, (pos[0] + shadow_offset, pos[1] + shadow_offset))
    surface.blit(font.render(text, True, color), pos)


def draw_next_button(surface, rect, hovered=False, label="Mulai Investigasi  →"):
    font = pygame.font.SysFont("Georgia", 18, bold=True)
    base = (200, 160, 40) if not hovered else (230, 190, 60)
    glow = (255, 220, 80)

    if hovered:
        glow_s = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        for i in range(6, 0, -1):
            a = i * 14
            r = i * 3
            pygame.draw.rect(
                glow_s, (*glow, a),
                pygame.Rect(10 - r, 10 - r, rect.width + r * 2, rect.height + r * 2),
                border_radius=14 + r,
            )
        surface.blit(glow_s, (rect.x - 10, rect.y - 10))

    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*base, 230), s.get_rect(), border_radius=12)
    surface.blit(s, rect.topleft)
    pygame.draw.rect(surface, glow if hovered else base, rect, border_radius=12, width=2)
    txt = font.render(label, True, (20, 14, 4) if not hovered else (10, 8, 2))
    surface.blit(txt, txt.get_rect(center=rect.center))


def draw_back_button(surface, rect, hovered=False):
    font = pygame.font.SysFont("Georgia", 15)
    base = (50, 50, 55) if hovered else (28, 28, 32)
    s    = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*base, 210), s.get_rect(), border_radius=10)
    surface.blit(s, rect.topleft)
    pygame.draw.rect(surface, (80, 80, 90) if hovered else (50, 50, 60), rect, border_radius=10, width=1)
    txt = font.render("← Kembali", True, (200, 200, 200))
    surface.blit(txt, txt.get_rect(center=rect.center))


def draw_verdict_button(surface, rect, text, color, hovered=False):
    font = pygame.font.SysFont("Georgia", 18, bold=True)
    c    = tuple(min(255, v + 40) for v in color) if hovered else color

    if hovered:
        glow_s = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
        for i in range(5, 0, -1):
            a = i * 12
            r = i * 2
            pygame.draw.rect(
                glow_s, (*c, a),
                pygame.Rect(8 - r, 8 - r, rect.width + r * 2, rect.height + r * 2),
                border_radius=14 + r,
            )
        surface.blit(glow_s, (rect.x - 8, rect.y - 8))

    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*c, 195), s.get_rect(), border_radius=12)
    surface.blit(s, rect.topleft)
    pygame.draw.rect(surface, c, rect, border_radius=12, width=2)
    txt = font.render(text, True, (255, 255, 255))
    surface.blit(txt, txt.get_rect(center=rect.center))
