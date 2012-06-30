import os, simplejson
import pygame

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
DEFAULT_FONT = 'Droid Sans'
DEFAULT_PALETTE = 'default'
FONT_CACHE = simplejson.load(open(os.path.join(FONT_DIR, 'fonts.json'), 'r'))

FONTS = {}

def get_font(font, size):
    name = font['ttf']
    if (name, size) not in FONTS:
        FONTS[name, size] = pygame.font.Font(os.path.join(FONT_DIR, name), size)
    return FONTS[name, size]

def load_font(name):
    for font in FONT_CACHE:
        if font['name'] == name:
            return font
    raise AttributeError('Invalid font name. Should be one of %s' % 
                         ", ".join([f['name'] for f in FONT_CACHE]))

