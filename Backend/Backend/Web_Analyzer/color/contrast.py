from colorsys import rgb_to_hsv

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b):
    a = [v / 255.0 for v in (r, g, b)]
    a = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in a]
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

def contrast_ratio(color1, color2):
    L1 = luminance(*color1)
    L2 = luminance(*color2)
    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)

text_color_hex = '#576EAF'
background_color_hex = '#000000'

text_color_rgb = hex_to_rgb(text_color_hex)
print(text_color_rgb)
background_color_rgb = hex_to_rgb(background_color_hex)
print(background_color_rgb)

ratio = contrast_ratio(text_color_rgb, background_color_rgb)
print(f"Contrast Ratio: {ratio:.2f}")