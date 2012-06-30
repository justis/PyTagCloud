def create_html_data(tags, 
        size=(500,500), 
        layout=LAYOUT_MIX, 
        fontname=DEFAULT_FONT,
        rectangular=False):
    """
    Create data structures to be used for HTML tag clouds.
    """

    if not len(tags):
        return

    sizeRect, tag_store = _draw_cloud(tags,
                                      layout,
                                      size=size, 
                                      fontname=fontname,
                                      rectangular=rectangular)

    tag_store = sorted(tag_store, key=lambda tag: tag.tag['size'])
    tag_store.reverse()
    data = {
            'css': {},
            'links': []
            }

    color_map = {}
    for color_index, tag in enumerate(tags):
        if not color_map.has_key(tag['color']):
            color_name = "c%d" % color_index
            hslcolor = colorsys.rgb_to_hls(tag['color'][0] / 255.0, 
                                           tag['color'][1] / 255.0, 
                                           tag['color'][2] / 255.0)
            lighter = hslcolor[1] * 1.4
            if lighter > 1: lighter = 1
            light = colorsys.hls_to_rgb(hslcolor[0], lighter, hslcolor[2])
            data['css'][color_name] = ('#%02x%02x%02x' % tag['color'], 
                                       '#%02x%02x%02x' % (light[0] * 255,
                                                          light[1] * 255,
                                                          light[2] * 255))
            color_map[tag['color']] = color_name

    for stag in tag_store:
        line_offset = 0

        line_offset = stag.font.get_linesize() - (stag.font.get_ascent() + \
                                                  abs(stag.font.get_descent()) - \
                                                  stag.rect.height) - 4

        tag = {
               'tag': stag.tag['tag'],
               'cls': color_map[stag.tag['color']],
               'top': stag.rect.y - sizeRect.y,
               'left': stag.rect.x - sizeRect.x,
               'size': int(stag.tag['size'] * 0.85),
               'height': int(stag.rect.height * 1.19) + 4,
               'width': stag.rect.width,
               'lh': line_offset
               }

        data['links'].append(tag)
        data['size'] = (sizeRect.w, sizeRect.h * 1.15)

    return data
