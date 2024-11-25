import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to fetch the webpage
def fetch_webpage(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to parse the HTML content
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Function to extract image information
def extract_images(soup):
    images = soup.find_all('img')
    image_info = []
    for img in images:
        src = img.get('src')
        srcset = img.get('srcset')
        sizes = img.get('sizes')
        format = src.split('.')[-1].lower() if src else 'unknown'
        lazy = 'loading' in img.attrs and img.attrs['loading'] == 'lazy'
        image_info.append({'src': src, 'srcset': srcset, 'sizes': sizes, 'format': format, 'lazy': lazy})
    return image_info

# Function to evaluate image formats
def evaluate_image_formats(image_info):
    format_scores = {
        'webp': 10, 'avif': 10, 'png': 7, 'jpg': 5, 'jpeg': 5,
        'gif': 4, 'svg': 9, 'heic': 8, 'heif': 8
    }
    evaluation = []
    for img in image_info:
        format = img['format']
        score = format_scores.get(format, 0)
        evaluation.append({'src': img['src'], 'format': format, 'score': score})
    return evaluation

# Function to extract meta tags
def extract_meta_tags(soup):
    meta_tags = soup.find_all('meta', attrs={'name': 'viewport'})
    return [meta.get('content') for meta in meta_tags]

# Function to evaluate viewport meta tag
def evaluate_viewport_meta(meta_tags):
    for tag in meta_tags:
        if 'width=device-width' in tag and 'initial-scale=1' in tag:
            return "Viewport meta tag is set correctly.", 10
    return "Viewport meta tag is missing or incorrect.", 0

# Function to evaluate responsive images
def evaluate_responsive_images(image_info):
    for img in image_info:
        if img['srcset']:
            return "Responsive images are used.", 10
    return "Responsive images are not used.", 0

# Function to evaluate lazy loading
def evaluate_lazy_loading(image_info):
    lazy_count = sum(1 for img in image_info if img['lazy'])
    if lazy_count > 0:
        return f"Lazy loading is used ({lazy_count} images).", 10
    return "Lazy loading is not used.", 0

# Function to extract CSS content
def extract_css(soup, base_url):
    styles = soup.find_all('style')
    links = soup.find_all('link', rel='stylesheet')
    css_content = [style.string for style in styles if style.string]
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            css_content.append(requests.get(full_url).text)
    return css_content

# Function to evaluate media queries
def evaluate_media_queries(css_content):
    media_query_count = sum(css.count('@media') for css in css_content)
    if media_query_count > 0:
        return f"Media queries are used ({media_query_count} found).", 10
    return "Media queries are not used.", 0

# Function to evaluate flexible grid layouts
def evaluate_flexible_layouts(css_content):
    flex_count = sum(css.count('display: flex') for css in css_content)
    grid_count = sum(css.count('display: grid') for css in css_content)
    if flex_count > 0 or grid_count > 0:
        return f"Flexible layouts are used (Flex: {flex_count}, Grid: {grid_count}).", 10
    return "Flexible layouts are not used.", 0

# Function to evaluate touch-friendly design
def evaluate_touch_friendly(soup):
    buttons = soup.find_all('button')
    links = soup.find_all('a')
    touch_friendly_count = sum(1 for btn in buttons if btn.get('style') and 'padding' in btn.get('style'))
    touch_friendly_count += sum(1 for link in links if link.get('style') and 'padding' in link.get('style'))
    if touch_friendly_count > 0:
        return f"Touch-friendly design is used ({touch_friendly_count} elements).", 10
    return "Touch-friendly design is not used.", 0

# Function to evaluate responsive typography
def evaluate_responsive_typography(css_content):
    rem_count = sum(css.count('rem') for css in css_content)
    em_count = sum(css.count('em') for css in css_content)
    if rem_count > 0 or em_count > 0:
        return f"Responsive typography is used (rem: {rem_count}, em: {em_count}).", 10
    return "Responsive typography is not used.", 0

# Main function
def responsive(html_content, css_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Evaluate Viewport Meta Tag
    meta_tags = extract_meta_tags(soup)
    viewport_evaluation, viewport_score = evaluate_viewport_meta(meta_tags)

    # Evaluate Responsive Images
    image_info = extract_images(soup)
    responsive_images_evaluation, responsive_images_score = evaluate_responsive_images(image_info)

    # Evaluate Lazy Loading
    lazy_loading_evaluation, lazy_loading_score = evaluate_lazy_loading(image_info)

    # Evaluate Media Queries
    media_queries_evaluation, media_queries_score = evaluate_media_queries(css_content)
    media_query_count = sum(css.count('@media') for css in css_content)

    # Evaluate Flexible Layouts
    flexible_layouts_evaluation, flexible_layouts_score = evaluate_flexible_layouts(css_content)
    flex_count = sum(css.count('display: flex') for css in css_content)
    grid_count = sum(css.count('display: grid') for css in css_content)

    # Evaluate Touch-Friendly Design
    touch_friendly_evaluation, touch_friendly_score = evaluate_touch_friendly(soup)
    touch_friendly_count = sum(1 for btn in soup.find_all('button') if btn.get('style') and 'padding' in btn.get('style'))
    touch_friendly_count += sum(1 for link in soup.find_all('a') if link.get('style') and 'padding' in link.get('style'))

    # Evaluate Responsive Typography
    responsive_typography_evaluation, responsive_typography_score = evaluate_responsive_typography(css_content)
    rem_count = sum(css.count('rem') for css in css_content)
    em_count = sum(css.count('em') for css in css_content)

    # Evaluate Image Formats
    image_format_evaluation = evaluate_image_formats(image_info)
    total_image_score = sum(img['score'] for img in image_format_evaluation)
    image_count = len(image_info)
    average_image_score = total_image_score / image_count if image_count > 0 else 0

    # Calculate Total Score
    total_score = (viewport_score + responsive_images_score + lazy_loading_score + 
                media_queries_score + flexible_layouts_score + touch_friendly_score +
                responsive_typography_score)

    results = {
        "viewport_evaluation": viewport_evaluation,
        "responsive_images_evaluation": responsive_images_evaluation,
        "lazy_loading_evaluation": lazy_loading_evaluation,
        "media_queries_evaluation": media_queries_evaluation,
        "flexible_layouts_evaluation": flexible_layouts_evaluation,
        "touch_friendly_evaluation": touch_friendly_evaluation,
        "responsive_typography_evaluation": responsive_typography_evaluation,
        "image_format_evaluation": image_format_evaluation,
        "total_score": total_score,
        "numerical_data": {
            "media_query_count": {"title": "Media Queries", "value": media_query_count},
            "average_image_score": {"title": "Average Image Score", "value": round(average_image_score)},
            "lazy_count": {"title": "Lazy Count", "value": lazy_loading_score},
            "touch_friendly_count": {"title": "Touch-friendly Count", "value": touch_friendly_count},
            "flex_count": {"title": "Flex Count", "value": flex_count},
            "grid_count": {"title": "Grid Count", "value": grid_count},
            "rem_count": {"title": "REM Count", "value": rem_count},
            "em_count": {"title": "EM Count", "value": em_count}
        },
        
        "one_liner_data": [
            { "title": "Viewport Meta Tag", "details": viewport_evaluation },
            { "title": "Lazy Loading", "details": lazy_loading_evaluation},
            { "title": "Media Queries", "details": media_queries_evaluation},
            { "title": "Flexible Layouts", "details": flexible_layouts_evaluation},
            { "title": "Touch-friendly", "details": touch_friendly_evaluation},
            { "title": "Responsive Typography", "details": responsive_typography_evaluation }
        ]
    }
    
    return results

