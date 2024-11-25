from colorsys import rgb_to_hsv

def hex_to_rgb(hex_color):
    if hex_color.startswith('#'):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6 and all(c in '0123456789abcdefABCDEF' for c in hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3 and all(c in '0123456789abcdefABCDEF' for c in hex_color):
            hex_color = ''.join([c*2 for c in hex_color])  # Convert 3-digit to 6-digit hex
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif hex_color.startswith('rgba(') and hex_color.endswith(')'):
        rgba = hex_color[5:-1].split(',')
        if len(rgba) == 4:
            try:
                return tuple(map(int, rgba[:3]))  # Ignore alpha value for contrast
            except ValueError:
                pass

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

from colorsys import rgb_to_hsv

def is_complementary(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs(h1 - h2) > 0.5

def is_analogous(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs(h1 - h2) < 0.1

def is_triadic(color1, color2):
    h1 = rgb_to_hsv(*color1)[0]
    h2 = rgb_to_hsv(*color2)[0]
    return abs((h1 - h2) * 3) % 1 < 0.1  # Rough check for triadic harmony

def color_harmony_score(color1, color2):
    if is_complementary(color1, color2):
        return 10
    elif is_analogous(color1, color2):
        return 7
    elif is_triadic(color1, color2):
        return 5
    else:
        return 2  # Clashing colors

def color_harmony(elements_properties):
    results = {}
    body_bg_color = elements_properties.get("body", {}).get("background-color")
    body_text_color = elements_properties.get("body", {}).get("color")
    
    if body_bg_color and body_text_color:
        body_bg_rgb = hex_to_rgb(body_bg_color)
        body_text_rgb = hex_to_rgb(body_text_color)
        
        if body_bg_rgb and body_text_rgb:
            harmony_score = color_harmony_score(body_bg_rgb, body_text_rgb)
            results["body_harmony_score"] = harmony_score

    for element, properties in elements_properties.items():
        if element != "body":
            bg_color = properties.get("background-color")
            text_color = properties.get("color")
            
            if bg_color and text_color:
                bg_rgb = hex_to_rgb(bg_color)
                text_rgb = hex_to_rgb(text_color)
                
                if bg_rgb and text_rgb:
                    harmony_score = color_harmony_score(bg_rgb, text_rgb)
                    results[f"{element}_harmony_score"] = harmony_score
                
                if body_text_color and bg_color:
                    body_text_rgb = hex_to_rgb(body_text_color)
                    if body_text_rgb and bg_rgb:
                        harmony_score = color_harmony_score(body_text_rgb, bg_rgb)
                        results[f"{element}_with_body_harmony_score"] = harmony_score
                        
    return results

def color_consistency(elements_properties):
    color_usage = {}

    for element, properties in elements_properties.items():
        bg_color = properties.get("background-color")
        text_color = properties.get("color")

        if bg_color and bg_color.startswith('#'):
            color_usage.setdefault(bg_color, []).append(f"{element}_background")
        
        if text_color and text_color.startswith('#'):
            color_usage.setdefault(text_color, []).append(f"{element}_text")
    
    return color_usage

def color_grading(elements_properties):
    results = {}
    color_usage = color_consistency(elements_properties)

    body_bg_color = elements_properties.get("body", {}).get("background-color")
    body_text_color = elements_properties.get("body", {}).get("color")

    if body_bg_color and body_text_color:
        body_bg_rgb = hex_to_rgb(body_bg_color)
        body_text_rgb = hex_to_rgb(body_text_color)
        if body_bg_rgb and body_text_rgb:
            results["body_contrast"] = contrast_ratio(body_bg_rgb, body_text_rgb)
            results["body_harmony_score"] = color_harmony_score(body_bg_rgb, body_text_rgb)

    # Check other visual elements
    for element, properties in elements_properties.items():
        if element != "body":
            bg_color = properties.get("background-color")
            text_color = properties.get("color")

            if bg_color and text_color:
                bg_rgb = hex_to_rgb(bg_color)
                text_rgb = hex_to_rgb(text_color)
                if bg_rgb and text_rgb:
                    results[f"{element}_contrast"] = contrast_ratio(bg_rgb, text_rgb)
                    results[f"{element}_harmony_score"] = color_harmony_score(bg_rgb, text_rgb)

            if body_text_color and bg_color:
                body_text_rgb = hex_to_rgb(body_text_color)
                if body_text_rgb and bg_rgb:
                    results[f"{element}_with_body_contrast"] = contrast_ratio(body_text_rgb, bg_rgb)
                    results[f"{element}_with_body_harmony_score"] = color_harmony_score(body_text_rgb, bg_rgb)

    results["color_consistency"] = color_usage
    return results