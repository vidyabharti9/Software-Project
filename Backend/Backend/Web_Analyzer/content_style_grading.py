from bs4 import BeautifulSoup

def check_alignment_counts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    alignment_counts = { 'total': len(elements), 'left': 0, 'center': 0, 'right': 0 }

    for element in elements:
        styles = element.get('style', '')
        if styles:
            style_dict = dict(item.split(":") for item in styles.split(";") if item)
            text_align = style_dict.get('text-align', '')

            if text_align == 'left' or text_align == 'start':
                alignment_counts['left'] += 1
            elif text_align == 'center':
                alignment_counts['center'] += 1
            elif text_align == 'right' or text_align == 'end':
                alignment_counts['right'] += 1
            else:
                parent = element.find_parent()
                if parent:
                    parent_styles = parent.get('style', '')
                    if parent_styles:
                        parent_style_dict = dict(item.split(":") for item in parent_styles.split(";") if item)
                        parent_text_align = parent_style_dict.get('text-align', '')
                        if parent_text_align == 'left' or parent_text_align == 'start':
                            alignment_counts['left'] += 1
                        elif parent_text_align == 'center':
                            alignment_counts['center'] += 1
                        elif parent_text_align == 'right' or parent_text_align == 'end':
                            alignment_counts['right'] += 1
                        else:
                            alignment_counts['left'] += 1  # Default to left if no alignment is found
                    else:
                        alignment_counts['left'] += 1  # Default to left if no alignment is found

    return alignment_counts


def check_flexbox_consistency(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    flexbox_counts = { 'total': len(elements), 'matching': 0 }
    flexbox_values = set()

    for element in elements:
        styles = element.get('style', '')
        if styles:
            style_dict = dict(item.split(":") for item in styles.split(";") if item)
            display = style_dict.get('display')
            justify_content = style_dict.get('justify-content')
            align_items = style_dict.get('align-items')

            if display == 'flex':
                flexbox_values.add(f'{justify_content}-{align_items}')

    if len(flexbox_values) == 1:
        flexbox_counts['matching'] = len(elements)
    else:
        first_flexbox = list(flexbox_values)[0] if flexbox_values else None
        for element in elements:
            styles = element.get('style', '')
            if styles:
                style_dict = dict(item.split(":") for item in styles.split(";") if item)
                current_flexbox = f'{style_dict.get("justify-content")}-{style_dict.get("align-items")}'
                if current_flexbox == first_flexbox:
                    flexbox_counts['matching'] += 1

    return flexbox_counts

def check_spacing_consistency(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    spacing_counts = { 'total': len(elements), 'matching': 0 }
    spacing_values = set()

    for element in elements:
        styles = element.get('style', '')
        if styles:
            style_dict = dict(item.split(":") for item in styles.split(";") if item)
            margin = f"{style_dict.get('margin-top', '0')}-{style_dict.get('margin-right', '0')}-{style_dict.get('margin-bottom', '0')}-{style_dict.get('margin-left', '0')}"
            padding = f"{style_dict.get('padding-top', '0')}-{style_dict.get('padding-right', '0')}-{style_dict.get('padding-bottom', '0')}-{style_dict.get('padding-left', '0')}"

            spacing_values.add(f"{margin}-{padding}")

    if spacing_values:
        if len(spacing_values) == 1:
            spacing_counts['matching'] = len(elements)
        else:
            first_spacing = list(spacing_values)[0]
            for element in elements:
                styles = element.get('style', '')
                if styles:
                    style_dict = dict(item.split(":") for item in styles.split(";") if item)
                    current_spacing = f"{style_dict.get('margin-top', '0')}-{style_dict.get('margin-right', '0')}-{style_dict.get('margin-bottom', '0')}-{style_dict.get('margin-left', '0')}-{style_dict.get('padding-top', '0')}-{style_dict.get('padding-right', '0')}-{style_dict.get('padding-bottom', '0')}-{style_dict.get('padding-left', '0')}"
                    if current_spacing == first_spacing:
                        spacing_counts['matching'] += 1

    return spacing_counts


def check_consistency(html_content):
    selectors = {
        'headers': 'h1, h2, h3, h4, h5, h6',
        'paragraphs': 'p',
        'images': 'img',
        'containers': 'div, section, article',
        'lists': 'ul, ol, li',
        'navigation': 'nav, ul, li'
    }

    consistency_report = {}

    for key, selector in selectors.items():
        try:
            alignment = check_alignment_counts(html_content)
            consistency_report[key] = {'alignment': alignment}
        except Exception as e:
            consistency_report[key] = {'alignment_error': str(e)}

        try:
            flexbox = check_flexbox_consistency(html_content)
            consistency_report[key].update({'flexbox': flexbox})
        except Exception as e:
            consistency_report[key].update({'flexbox_error': str(e)})

        try:
            spacing = check_spacing_consistency(html_content)
            consistency_report[key].update({'spacing': spacing})
        except Exception as e:
            consistency_report[key].update({'spacing_error': str(e)})

    return consistency_report

# Define serif and sans-serif font lists
serif_fonts = ['Times New Roman', 'Georgia', 'Garamond', 'Palatino', 'Book Antiqua']
sans_serif_fonts = ['Arial', 'Helvetica', 'Verdana', 'Tahoma', 'Trebuchet MS']

# Function to evaluate visual harmony
def evaluate_visual_harmony(font_families):
    serif_count = sum(1 for font in font_families if any(serif in font for serif in serif_fonts))
    sans_serif_count = sum(1 for font in font_families if any(sans_serif in font for sans_serif in sans_serif_fonts))
    
    # Check for typeface consistency
    typeface_counts = {}
    for font in font_families:
        base_font = font.split(',')[0].strip()  # Get the base typeface name
        if base_font in typeface_counts:
            typeface_counts[base_font] += 1
        else:
            typeface_counts[base_font] = 1
    
    # Calculate harmony score
    harmony_score = min(serif_count, sans_serif_count) + sum(1 for count in typeface_counts.values() if count > 1)
    return harmony_score

def font_harmony(elements_properties):
    font_families = []

    # Extract font families from elements_properties
    for element, properties in elements_properties.items():
        font_family = properties.get("font-family")
        if font_family and 'var' not in font_family and font_family != "null":
            font_families.append(font_family)

    harmony_score = evaluate_visual_harmony(font_families)
    return {"font_harmony_score": harmony_score}
