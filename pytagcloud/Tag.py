from copy import copy
from pygame.sprite import Sprite
import pygame
from . import fonts

TAG_PADDING = 5

convsurf = pygame.Surface((2 * TAG_PADDING, 2 * TAG_PADDING))
convsurf.fill((255, 0, 255))
convsurf.set_colorkey((255, 0, 255))
pygame.draw.circle(convsurf, (0, 0, 0), (TAG_PADDING, TAG_PADDING), TAG_PADDING)
CONVMASK = pygame.mask.from_surface(convsurf)


class Tag(Sprite):
    """
    Font tag sprite. Blit the font to a surface to correct the font padding
    """
    def __init__(self, tag, initial_position, fontname=fonts.DEFAULT_FONT):
        Sprite.__init__(self)
        self.tag = copy(tag)
        self.rotation = 0
        
        self.font_spec = fonts.load_font(fontname)
        self.font = fonts.get_font(self.font_spec, self.tag['size'])
        fonter = self.font.render(tag['tag'], True, tag['color'])
        frect = fonter.get_bounding_rect()
        frect.x = -frect.x
        frect.y = -frect.y
        self.fontoffset = (-frect.x, -frect.y)
        font_sf = pygame.Surface((frect.width, frect.height), pygame.SRCALPHA, 32)
        font_sf.blit(fonter, frect)
        self.image = font_sf
        self.rect = font_sf.get_rect()
        self.rect.width += TAG_PADDING
        self.rect.height += TAG_PADDING
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]
        self._update_mask()

    def _update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = self.mask.convolve(CONVMASK, None, (TAG_PADDING, TAG_PADDING))

    def flip(self):
        angle = 90 if self.rotation == 0 else - 90
        self.rotate(angle)

    def rotate(self, angle):
        pos = (self.rect.x, self.rect.y)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self._update_mask()

    def update_fontsize(self):
        self.font = fonts.get_font(self.font_spec, self.tag['size'])
