# -*- coding: utf-8 -*-
from math import sin, cos, ceil
from pygame import transform, font, mask, Surface, Rect, SRCALPHA, draw
from pygame.sprite import Group, Sprite, collide_mask
from random import randint, choice
import colorsys
import math
import os
import pygame
import simplejson
from . import Tag, fonts, placement

__all__ = [ 'Tag', 'placement', 'fonts' ]

STEP_SIZE = 2 # relative to base step size of each spiral function
RADIUS = 1
ECCENTRICITY = 1.5

LOWER_START = 0.45
UPPER_START = 0.55

pygame.init()

LAYOUT_HORIZONTAL = 0
LAYOUT_VERTICAL = 1
LAYOUT_MOST_HORIZONTAL = 2
LAYOUT_MOST_VERTICAL = 3
LAYOUT_MIX = 4

LAYOUTS = (
           LAYOUT_HORIZONTAL,
           LAYOUT_VERTICAL,
           LAYOUT_MOST_HORIZONTAL,
           LAYOUT_MOST_VERTICAL,
           LAYOUT_MIX
           )

def defscale(count, mincount, maxcount, minsize, maxsize):
    if maxcount == mincount:
        return int((maxsize - minsize) / 2.0 + minsize)
    return int(minsize + (maxsize - minsize) * 
               (count * 1.0 / (maxcount - mincount)) ** 0.8)

def make_tags(wordcounts, minsize=3, maxsize=36, colors=None, scalef=defscale):
    """
    sizes and colors tags 
    wordcounts is a list of tuples(tags, count). (e.g. how often the
    word appears in a text)
    the tags are assigned sizes between minsize and maxsize, the function used
    is determined by scalef (default: square root)
    color is either chosen from colors (list of rgb tuples) if provided or random
    """
    counts = [tag[1] for tag in wordcounts]

    if not len(counts):
        return []

    maxcount = max(counts)
    mincount = min(counts)
    tags = []
    for word_count in wordcounts:
        color = choice(colors) if colors else (randint(10, 220), randint(10, 220),
                                               randint(10, 220))
        tags.append({'color': color, 'size': scalef(word_count[1], mincount,
                                                    maxcount, minsize, maxsize),
                     'tag': word_count[0]})
    return tags

def _draw_cloud(
        tag_list,
        layout=LAYOUT_MIX,
        size=(500,500),
        fontname=fonts.DEFAULT_FONT,
        rectangular=False):

    # sort the tags by size and word length
    tag_list.sort(key=lambda tag: len(tag['tag']))
    tag_list.sort(key=lambda tag: tag['size'])
    tag_list.reverse()

    # create the tag space
    tag_sprites = []
    area = 0
    for tag in tag_list:
        tag_sprite = Tag.Tag(tag, (0, 0), fontname=fontname)
        area += tag_sprite.mask.count()
        tag_sprites.append(tag_sprite)

    canvas = Rect(0, 0, 0, 0)
    ratio = float(size[1]) / size[0]

    if rectangular:
        spiral = placement._rectangular_spiral
    else:
        spiral = placement._archimedean_spiral

    aligned_tags = Group()
    for tag_sprite in tag_sprites:
        angle = 0
        if layout == LAYOUT_MIX and randint(0, 2) == 0:
            angle = 90
        elif layout == LAYOUT_VERTICAL:
            angle = 90

        tag_sprite.rotate(angle)

        xpos = canvas.width - tag_sprite.rect.width
        if xpos < 0: xpos = 0
        xpos = randint(int(xpos * LOWER_START) , int(xpos * UPPER_START))
        tag_sprite.rect.x = xpos

        ypos = canvas.height - tag_sprite.rect.height
        if ypos < 0: ypos = 0
        ypos = randint(int(ypos * LOWER_START), int(ypos * UPPER_START))
        tag_sprite.rect.y = ypos

        placement._search_place(tag_sprite, aligned_tags, canvas, spiral, ratio)

    canvas = placement._get_tags_bounding(aligned_tags)
    zoom = min(float(size[0]) / canvas.w, float(size[1]) / canvas.h)
    _resize_cloud(aligned_tags, zoom)

    # get resized canvas
    canvas = placement._get_tags_bounding(aligned_tags)

    return canvas, aligned_tags

def _resize_cloud(aligned_tags, zoom):
    for tag in aligned_tags:
        tag.rect.x *= zoom
        tag.rect.y *= zoom
        tag.rect.width *= zoom
        tag.rect.height *= zoom
        tag.tag['size'] = int(tag.tag['size'] * zoom)
        tag.update_fontsize() 

def create_tag_image(
        tags, 
        output, 
        size=(500,500), 
        background=(255, 255, 255), 
        layout=LAYOUT_MIX, 
        fontname=fonts.DEFAULT_FONT,
        rectangular=False):
    """
    Create a png tag cloud image
    """

    if not len(tags):
        return

    sizeRect, tag_store = _draw_cloud(tags,
                                      layout,
                                      size=size, 
                                      fontname=fontname,
                                      rectangular=rectangular)

    if type(output) == pygame.Surface:
        image_surface = output
    else:
        image_surface = Surface((sizeRect.w, sizeRect.h), SRCALPHA, 32)
        image_surface.fill(background)
    for tag in tag_store:
        image_surface.blit(tag.image, tag.rect)
    pygame.image.save(image_surface, output)
    return tag_store

def draw_tags(tag_store, target_surface, background=(255,255,255)):
    for tag in tag_store:
        #pygame.draw.rect(target_surface, (0,255,0), tag.rect)
        target_surface.blit(tag.image, tag.rect)
