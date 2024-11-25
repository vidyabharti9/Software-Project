import cssutils
from colour import Color

class CssColorExtractor:
    def __init__(self):
        self.properties_with_colors = [
            'color', 'background', 'background-color', 'background-image', 'border', 'border-top',
            'border-right', 'border-bottom', 'border-left', 'border-color', 'border-top-color',
            'border-right-color', 'border-bottom-color', 'border-left-color', 'outline',
            'outline-color', 'text-decoration', 'text-decoration-color', 'text-shadow',
            'box-shadow', 'fill', 'stroke', 'stop-color', 'flood-color', 'lighting-color',
        ]
        self.color_formats = [
            'hex', 'rgb', 'hsl', 'hwb', 'name',
        ]

    def does_property_allow_color(self, property):
        return property in self.properties_with_colors

    def is_color_grey(self, color):
        red = color.red * 255
        return self.is_color_monochrome(color) and 0 < red < 255

    def is_color_monochrome(self, color):
        return color.hsl[1] == 0

    def is_valid_color_format(self, format):
        return format in self.color_formats

    def serialize_color(self, value, options):
        if not options.get('color_format') or not self.is_valid_color_format(options['color_format']):
            return value

        color = Color(value)
        color_format = options['color_format']
        
        if color_format == 'name' and color.get_name():
            return color.get_name()
        
        if hasattr(color, color_format):
            formatted = getattr(color, color_format)
            if callable(formatted):
                return formatted()
            return formatted
        return value

    def default_options(self, options):
        return {
            'without_grey': False,
            'without_monochrome': False,
            'all_colors': False,
            'color_format': None,
            'sort': None,
            **options,
        }

    def sort_colors(self, colors, sort_options):
        options = self.default_options(sort_options)
        colors = [self.serialize_color(color, options) for color in colors]
        
        if options['sort'] == 'hue':
            colors.sort(key=lambda c: Color(c).hue)
        
        if options['sort'] == 'frequency':
            from collections import Counter
            frequency = Counter(colors)
            colors.sort(key=lambda x: -frequency[x])
        
        return colors if options['all_colors'] else list(set(colors))

    def extract_colors_from_string(self, string, options):
        colors = []
        options = self.default_options(options)

        import re
        items = re.split(r',\s*', string)
        for item in items:
            subitems = item.split()
            for subitem in subitems:
                match = re.match(r'^(?:-webkit-|-moz-|-o-)?(?:repeating-)?(?:radial|linear)-gradient\((.*?)\)$', subitem)
                if match:
                    colors.extend(re.split(r',\s*', match.group(1)))
                else:
                    colors.append(subitem)

        def is_valid_color(value):
            try:
                color = Color(value)
                if options['without_monochrome'] and self.is_color_monochrome(color):
                    return False
                if options['without_grey'] and self.is_color_grey(color):
                    return False
                if options['color_format'] == 'name' and not color.get_name():
                    return False
                return True
            except ValueError:
                return False

        return [color for color in colors if is_valid_color(color)]

    def extract_colors_from_decl(self, decl, options):
        if not self.does_property_allow_color(decl.name):
            return []
        return self.extract_colors_from_string(decl.value, options)

    def extract_colors_from_css(self, css, options):
        colors = []
        sheet = cssutils.parseString(css)

        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    colors.extend(self.extract_colors_from_decl(property, options))

        return colors

    def from_decl(self, decl, options={}):
        return self.sort_colors(self.extract_colors_from_decl(decl, options), options)

    def from_css(self, css, options={}):
        return self.sort_colors(self.extract_colors_from_css(css, options), options)

    def from_string(self, string, options={}):
        return self.sort_colors(self.extract_colors_from_string(string, options), options)


# Example usage
if __name__ == "__main__":
    extractor = CssColorExtractor()

    css = """
    .example {
        color: #ff0000;
        background: linear-gradient(to right, #ff0000, #00ff00);
        border: 1px solid rgb(0, 0, 255);
    }
    """

    options = {
        'without_grey': False,
        'without_monochrome': False,
        'all_colors': True,
        'color_format': 'hex',
        'sort': 'frequency',
    }

    extracted_colors = extractor.from_css(css, options)
    print(extracted_colors)
