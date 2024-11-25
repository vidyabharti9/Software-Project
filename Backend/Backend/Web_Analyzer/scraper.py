import re
import urllib.parse
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup

import re
import urllib.parse
from typing import Optional, List, Dict, Tuple
import requests
from bs4 import BeautifulSoup

def extract_css_from_webpage(
    url: str, request_kwargs: Optional[dict] = None, verbose: bool = False
) -> Tuple[List[str], List[str], List[Dict[str, str]]]:
    """Extracts CSS from webpage

    Args:
        url (str): Webpage URL
        request_kwargs (dict): These arguments are passed to requests.get() (when
                                fetching webpage HTML and external stylesheets)
        verbose (bool): Print diagnostic information

    Returns:
        tuple[ list[str], list[str], list[dict] ]: css_from_external_stylesheets, css_from_style_tags, inline_css
    """

    if not request_kwargs:
        request_kwargs = {
            "timeout": 10,
            "headers": {"User-Agent": "Definitely not an Automated Script"},
        }
    url_response = requests.get(url, **request_kwargs)
    if url_response.status_code != 200:
        raise requests.exceptions.HTTPError(
            f"received response [{url_response.status_code}] from [{url}]"
        )

    soup = BeautifulSoup(url_response.content, "html.parser")

    css_from_external_stylesheets: List[str] = []
    for link in soup.find_all("link", rel="stylesheet"):
        css_url = urllib.parse.urljoin(url, link["href"])
        if verbose:
            print(f"downloading external CSS stylesheet {css_url}")
        css_content: str = requests.get(css_url, **request_kwargs).text
        css_from_external_stylesheets.append(css_content)

    css_from_style_tags: List[str] = []
    for style_tag in soup.find_all("style"):
        css_from_style_tags.append(style_tag.string)

    inline_css: List[Dict[str, str]] = []
    for tag in soup.find_all(style=True):
        inline_css.append({"tag": str(tag), "css": tag["style"]})

    if verbose:
        print(
            f"""Extracted the following CSS from [{url}]:
    1. {len(css_from_external_stylesheets):,} external stylesheets (total {len("".join(css_from_external_stylesheets)):,} characters of text)
    2. {len(css_from_style_tags):,} style tags (total {len("".join(css_from_style_tags)):,} characters of text)
    3. {len(inline_css):,} tags with inline CSS (total {len("".join( (x["css"] for x in inline_css) )):,} characters of text)

"""
        )

    return css_from_external_stylesheets, css_from_style_tags, inline_css

def parse_css_rules(css: str) -> List[Dict[str, str]]:
    rules = []
    pattern = re.compile(r'([^{]+)\{([^}]+)\}')
    for match in pattern.finditer(css):
        selector = match.group(1).strip()
        properties = match.group(2).strip().split(';')
        rule = {'selector': selector, 'properties': {}}
        for prop in properties:
            if ':' in prop:
                name, value = prop.split(':', 1)  # Split only on the first colon
                rule['properties'][name.strip()] = value.strip()
        rules.append(rule)
    return rules

def extract_all_vars(css_rules: List[Dict[str, str]]) -> Dict[str, str]:
    var_pattern = re.compile(r'--[\w-]+')
    all_vars = {}
    for rule in css_rules:
        for prop, value in rule['properties'].items():
            if var_pattern.match(prop):
                all_vars[prop] = value
    return all_vars

def resolve_nested_vars(value: str, all_vars: Dict[str, str]) -> str:
    while value.startswith('var('):
        var_name = value[4:-1].strip()
        if var_name in all_vars:
            value = all_vars[var_name]
        else:
            break
    return value

def replace_vars_with_values(properties: Dict[str, Optional[str]], all_vars: Dict[str, str]) -> Dict[str, Optional[str]]:
    for prop, value in properties.items():
        if value:
            properties[prop] = resolve_nested_vars(value, all_vars)
    return properties

def extract_typography_properties(element, css_rules, properties_to_extract: List[str], all_vars: Dict[str, str]) -> Dict[str, Optional[str]]:
    properties = {prop: None for prop in properties_to_extract}
    for rule in css_rules:
        if element.name in rule['selector']:
            for prop in properties.keys():
                if properties[prop] is None and prop in rule['properties']:
                    properties[prop] = rule['properties'][prop]
    # Replace var() with actual values from all_vars
    properties = replace_vars_with_values(properties, all_vars)
    return properties

def find_properties(url: str, properties_to_extract: List[str]) -> Dict[str, Dict[str, Optional[str]]]:
    css_from_external_stylesheets, css_from_style_tags, inline_css = extract_css_from_webpage(url)

    css_rules = []
    for css in css_from_external_stylesheets + css_from_style_tags:
        css_rules.extend(parse_css_rules(css))

    # Extract all variables
    all_vars = extract_all_vars(css_rules)

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    elements_properties = {}
    for element in soup.find_all(True):
        properties = extract_typography_properties(element, css_rules, properties_to_extract, all_vars)
        elements_properties[element.name] = properties

    return elements_properties
