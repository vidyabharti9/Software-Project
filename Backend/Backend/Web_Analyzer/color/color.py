import requests
from bs4 import BeautifulSoup
import cssutils

def extract_colors_from_css(css_content):
    parser = cssutils.CSSParser()
    stylesheet = parser.parseString(css_content)
    colors = {}
    for rule in stylesheet:
        if rule.type == rule.STYLE_RULE:
            for property in rule.style:
                if property.name in ['color', 'background-color']:
                    selector = rule.selectorText
                    if selector not in colors:
                        colors[selector] = {}
                    colors[selector][property.name] = property.value
    return colors

def extract_colors_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    colors = {}
    for tag in soup.find_all(style=True):
        style = tag['style']
        tag_name = tag.name
        if tag_name not in colors:
            colors[tag_name] = {}
        if 'color' in style:
            colors[tag_name]['color'] = style.split('color:')[1].split(';')[0].strip()
        if 'background-color' in style:
            colors[tag_name]['background_color'] = style.split('background-color:')[1].split(';')[0].strip()
    return colors

def scrape_colors(url):
    response = requests.get(url)
    html_content = response.text

    html_colors = extract_colors_from_html(html_content)

    css_content = response.content.decode('utf-8')
    css_colors = extract_colors_from_css(css_content)

    return html_colors, css_colors

url = 'https://google.com'
html_colors, css_colors = scrape_colors(url)

print("HTML Colors:")
for tag, styles in html_colors.items():
    print(f"Tag: {tag}, Styles: {styles}")

print("\nCSS Colors:")
for selector, styles in css_colors.items():
    print(f"Selector: {selector}, Styles: {styles}")

colors_data = {
    'body': {
        'text_color': html_colors.get('body', {}).get('color', ''),
        'background_color': html_colors.get('body', {}).get('background_color', '')
    },
    'h1': {
        'text_color': css_colors.get('h1', {}).get('color', '')
    },
    'mark': {
        'highlight_color': css_colors.get('.mark', {}).get('color', ''),
        'highlight_bg': css_colors.get('.mark', {}).get('background-color', '')
    },
    'a': {
        'link_color': css_colors.get('a', {}).get('color', ''),
        'hover_color': css_colors.get('a:hover', {}).get('color', '')
    }
    # Add more elements as needed
}

for element, styles in colors_data.items():
    print(f"{element}: {styles}")
