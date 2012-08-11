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
        self.position = initial_position
        
        self.font_spec = fonts.load_font(fontname)
        self.font = fonts.get_font(self.font_spec, self.tag['size'])
        self.draw()

    def draw(self, surface=None):
        fonter = self.font.render(self.tag['tag'], True, self.tag['color'])
        frect = fonter.get_bounding_rect()
        frect.x = -frect.x
        frect.y = -frect.y
        self.fontoffset = (-frect.x, -frect.y)
        font_sf = pygame.Surface((frect.width, frect.height), pygame.SRCALPHA, 32)
        font_sf.blit(fonter, frect)
        if False:
            surface.blit(fonter, frect)
            self._update_mask()
            return
            
        self.image = font_sf
        if not hasattr(self, 'rect'):
            self.rect = font_sf.get_rect()
            self.rect.width += TAG_PADDING
            self.rect.height += TAG_PADDING
            self.rect.x, self.rect.y = self.position
        else:
            old_rect = self.rect
            self.rect = font_sf.get_rect()
            self.rect.width += TAG_PADDING
            self.rect.height += TAG_PADDING
            #self.rect.x, self.rect.y = old_rect.x, old_rect.y
            #self.rect.x, self.rect.y = self.box2d_body.b2body.position
            #print self.box2d_body.position
            
        self._update_mask()

    def _update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = self.mask.convolve(CONVMASK, None, (TAG_PADDING, TAG_PADDING))

    def flip(self):
        angle = 90 if self.rotation == 0 else - 90
        self.rotate(angle)

    def rotate(self, angle):
        #pos = (self.rect.x, self.rect.y)
        self.image = pygame.transform.rotate(self.image, angle)
        #self.rect = self.image.get_rect()
        #self.rect.x, self.rect.y = pos
        self._update_mask()

    def update_fontsize(self, scale=1.0):
        size = int(self.tag['size'] * scale)
        if size < 10: size = 10
        #size = 30
        self.font = fonts.get_font(self.font_spec, size)
