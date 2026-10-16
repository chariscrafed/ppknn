import pygame


class ImageButton:
    """Button with image-based rendering and hover effects."""

    def __init__(self, image, hover, x, y, text, font):
        self.image = image
        self.hover = hover
        self.current = image
        self.rect = self.image.get_rect(center=(x, y))
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        self.current = self.hover if self.rect.collidepoint(mouse) else self.image

        screen.blit(self.current, self.rect)

        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow.set_alpha(120)
        screen.blit(
            shadow,
            (
                self.rect.centerx - shadow.get_width() // 2 + 2,
                self.rect.centery - shadow.get_height() // 2 + 2,
            ),
        )

        txt = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False