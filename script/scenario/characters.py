def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

CHARACTERS = {
    "male": {"name": "Внутренний голос", "color": hex_to_rgb("#B3DCFD")},
    "male_speak": {"name": "", "color": hex_to_rgb("#B3DCFD")},
    "tamara": {"name": "Препод Тамара", "color": hex_to_rgb("#E2633F")},
    "tamarochka": {"name": "Тамара", "color": hex_to_rgb("#E2633F")},
    "tamara_prepod": {"name": "Преподаватель ", "color": hex_to_rgb("#E2633F")},
    "system": {"name": "", "color": hex_to_rgb("#A9A9A9")}
}