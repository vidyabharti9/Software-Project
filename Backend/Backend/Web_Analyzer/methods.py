import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import nest_asyncio
import aiohttp
import asyncio
from urllib.parse import urlparse

nest_asyncio.apply()

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            status = response.status
            return {
                "url": url,
                "status": status,
                "message": response.reason
            }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "message": str(e)
        }

async def check_links(base_url):
    results = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(base_url)
        soup = BeautifulSoup(await response.text(), 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        tasks = []
        for link in links:
            if link.startswith('#'):
                continue
            if not urlparse(link).scheme:
                link = urljoin(base_url, link)
            if link.startswith('http'):
                tasks.append(fetch(session, link))
            else:
                results.append({
                    "url": link,
                    "status": "skipped",
                    "message": "Non-HTTP URL"
                })
        responses = await asyncio.gather(*tasks)
        results.extend(responses)
    return results

def run_link_checker(base_url):
    return asyncio.run(check_links(base_url))

def check_alignment_counts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    alignment_counts = {'total': len(elements), 'left': 0, 'center': 0, 'right': 0}

    for element in elements:
        style = element.get('style', '')
        text_align = None
        if 'text-align' in style:
            text_align = style.split('text-align:')[1].split(';')[0].strip()
        
        if text_align == 'left' or text_align == 'start':
            alignment_counts['left'] += 1
        elif text_align == 'center':
            alignment_counts['center'] += 1
        elif text_align == 'right' or text_align == 'end':
            alignment_counts['right'] += 1
        else:
            parent = element.find_parent()
            if parent:
                parent_style = parent.get('style', '')
                if 'text-align' in parent_style:
                    parent_text_align = parent_style.split('text-align:')[1].split(';')[0].strip()
                    if parent_text_align == 'left' or parent_text_align == 'start':
                        alignment_counts['left'] += 1
                    elif parent_text_align == 'center':
                        alignment_counts['center'] += 1
                    elif parent_text_align == 'right' or parent_text_align == 'end':
                        alignment_counts['right'] += 1
                    else:
                        alignment_counts['left'] += 1
                else:
                    alignment_counts['left'] += 1
            else:
                alignment_counts['left'] += 1

    return alignment_counts

def check_flexbox_consistency(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    flexbox_counts = {'total': len(elements), 'matching': 0}
    flexbox_values = set()

    for element in elements:
        style = element.get('style', '')
        display = None
        justify_content = None
        align_items = None
        if 'display' in style:
            display = style.split('display:')[1].split(';')[0].strip()
        if 'justify-content' in style:
            justify_content = style.split('justify-content:')[1].split(';')[0].strip()
        if 'align-items' in style:
            align_items = style.split('align-items:')[1].split(';')[0].strip()

        if display == 'flex':
            flexbox_values.add(f'{justify_content}-{align_items}')

    if len(flexbox_values) == 1:
        flexbox_counts['matching'] = len(elements)
    else:
        first_flexbox = f'{justify_content}-{align_items}' if elements else None
        for element in elements:
            style = element.get('style', '')
            current_flexbox = f'{justify_content}-{align_items}'
            if current_flexbox == first_flexbox:
                flexbox_counts['matching'] += 1

    return flexbox_counts

def check_spacing_consistency(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(True)
    spacing_counts = {'total': len(elements), 'matching': 0}
    spacing_values = set()

    for element in elements:
        style = element.get('style', '')
        margin = None
        padding = None
        if 'margin' in style:
            margin = style.split('margin:')[1].split(';')[0].strip()
        if 'padding' in style:
            padding = style.split('padding:')[1].split(';')[0].strip()

        spacing_values.add(f'{margin}-{padding}')

    if len(spacing_values) == 1:
        spacing_counts['matching'] = len(elements)
    else:
        first_spacing = f'{margin}-{padding}' if elements else None
        for element in elements:
            style = element.get('style', '')
            current_spacing = f'{margin}-{padding}'
            if current_spacing == first_spacing:
                spacing_counts['matching'] += 1

    return spacing_counts

def fetch_webpage(url, retries=3, delay=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 503:
            print(f"503 Service Unavailable. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            return None
    return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_css_js_files(soup, base_url):
    css_files = [urljoin(base_url, link.get('href')) for link in soup.find_all('link', rel='stylesheet')]
    js_files = [urljoin(base_url, script.get('src')) for script in soup.find_all('script') if script.get('src')]

    # Extract internal CSS and JS
    internal_css = [style.string for style in soup.find_all('style') if style.string]
    internal_js = [script.string for script in soup.find_all('script') if script.string]

    return css_files, js_files, internal_css, internal_js

def get_file_size(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.head(url, headers=headers)
    if response.status_code == 200:
        content_length = response.headers.get('Content-Length')
        if content_length:
            return int(content_length)
        else:
            # Fallback to GET request if Content-Length is not provided
            response = requests.get(url, headers=headers)
            return len(response.content)
    return 0

def evaluate_file_sizes(css_files, js_files, internal_css, internal_js):
    total_css_size = sum(get_file_size(url) for url in css_files) + sum(len(css) for css in internal_css)
    total_js_size = sum(get_file_size(url) for url in js_files) + sum(len(js) for js in internal_js)
    return total_css_size, total_js_size


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

    # Evaluate Flexible Layouts
    flexible_layouts_evaluation, flexible_layouts_score = evaluate_flexible_layouts(css_content)

    # Evaluate Touch-Friendly Design
    touch_friendly_evaluation, touch_friendly_score = evaluate_touch_friendly(soup)

    # Evaluate Responsive Typography
    responsive_typography_evaluation, responsive_typography_score = evaluate_responsive_typography(css_content)

    # Evaluate Image Formats
    image_format_evaluation = evaluate_image_formats(image_info)

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
        "total_score": total_score
    }
    
    return results
