import random, pygame, math

STEP_SIZE = 2 # relative to base step size of each spiral function
RADIUS = 1
ECCENTRICITY = 1.5

def _archimedean_spiral(reverse):
    DEFAULT_STEP = 0.05 # radians
    t = 0
    r = 1
    if reverse:
        r = -1
    while True:
        t += DEFAULT_STEP * STEP_SIZE * r
        yield (ECCENTRICITY * RADIUS * t * math.cos(t), RADIUS * t * math.sin(t))

def _rectangular_spiral(reverse):
    DEFAULT_STEP = 3 # px
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if reverse:
        directions.reverse()
    direction = directions[0]

    spl = 1
    dx = dy = 0
    while True:
        for step in range(spl * 2):
            if step == spl:
                direction = directions[(spl - 1) % 4]
            dx += direction[0] * STEP_SIZE * DEFAULT_STEP
            dy += direction[1] * STEP_SIZE * DEFAULT_STEP
            yield dx, dy
        spl += 1

def _search_place(current_tag, tag_store, canvas, spiral, ratio):
    """
    Start a spiral search with random direction.
    Resize the canvas if the spiral exceeds the bounding rectangle
    """

    reverse = random.choice((0, 1))
    start_x = current_tag.rect.x
    start_y = current_tag.rect.y
    min_dist = None
    opt_x = opt_y = 0
    
    current_bounding = _get_tags_bounding(tag_store)
    cx = current_bounding.w / 2.0
    cy = current_bounding.h / 2.0

    for dx, dy in spiral(reverse):
        current_tag.rect.x = start_x + dx
        current_tag.rect.y = start_y + dy
        if not _do_collide(current_tag, tag_store):
            if canvas.contains(current_tag.rect):
                tag_store.add(current_tag)
                return
            else:
                # get the distance from center
                current_dist = (abs(cx - current_tag.rect.x) ** 2 + 
                                abs(cy - current_tag.rect.y) ** 2) ** 0.5
                if not min_dist or current_dist < min_dist:
                    opt_x = current_tag.rect.x
                    opt_y = current_tag.rect.y 
                    min_dist = current_dist

                # only add tag if the spiral covered the canvas boundaries
                if abs(dx) > canvas.width / 2.0 and abs(dy) > canvas.height / 2.0:
                    current_tag.rect.x = opt_x                    
                    current_tag.rect.y = opt_y                    
                    tag_store.add(current_tag)

                    new_bounding = current_bounding.union(current_tag.rect)

                    delta_x = delta_y = 0.0
                    if new_bounding.w > canvas.width:
                        delta_x = new_bounding.w - canvas.width

                        canvas.width = new_bounding.w
                        delta_y = ratio * new_bounding.w - canvas.height
                        canvas.height = ratio * new_bounding.w

                    if new_bounding.h > canvas.height:
                        delta_y = new_bounding.h - canvas.height

                        canvas.height = new_bounding.h
                        canvas.width = new_bounding.h / ratio
                        delta_x = canvas.width - canvas.width

                    # realign
                    for tag in tag_store:
                        tag.rect.x += delta_x / 2.0
                        tag.rect.y += delta_y / 2.0


                    canvas = _get_tags_bounding(tag_store)

                    return

LAST_COLLISON_HIT = None

def _do_collide(sprite, group):
    """
    Use mask based collision detection
    """
    global LAST_COLLISON_HIT
    # Test if we still collide with the last hit
    if LAST_COLLISON_HIT and pygame.sprite.collide_mask(sprite, LAST_COLLISON_HIT):
        return True
    
    for sp in group:
        if pygame.sprite.collide_mask(sprite, sp):
            LAST_COLLISON_HIT = sp
            return True
    return False

def _get_tags_bounding(tag_store):
    if not len(tag_store):
        return pygame.Rect(0,0,0,0)
    rects = [tag.rect for tag in tag_store]
    return rects[0].unionall(rects[1:])

def _get_group_bounding(tag_store, sizeRect):
    if not isinstance(sizeRect, pygame.Rect):
        sizeRect = pygame.Rect(0, 0, sizeRect[0], sizeRect[1])
    if tag_store:
        rects = [tag.rect for tag in tag_store]
        union = rects[0].unionall(rects[1:])
        if sizeRect.contains(union):
            return union
    return sizeRect

