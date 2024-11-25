from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from urllib.parse import urlparse

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def is_valid_robots_content(content):
    # Basic validation for common robots.txt lines (User-agent, Disallow, Allow, Sitemap)
    lines = content.splitlines()
    for line in lines:
        if line.strip().startswith(("User-agent", "Disallow", "Allow", "Sitemap", "Crawl-delay", "Host")):
            return True
    return False

def check_robots_txt(base_url):
    robots_url = base_url + "/robots.txt"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Send request with a User-Agent header to mimic a browser
        response = requests.get(robots_url, headers=headers, allow_redirects=True)

        # Check if the status code is 200 (OK)
        if response.status_code == 200:
            # Check if the content of the robots.txt follows standard patterns
            if is_valid_robots_content(response.text):
                return True
            else:
                return False  # Not a valid robots.txt format
        elif response.status_code == 404:
            return "robots.txt file not found"
        elif response.status_code == 403:
            return "access to robots.txt is forbidden"
        elif response.status_code == 529:
            return "server error"
        else:
            return f"unexpected status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Error checking robots.txt: {e}"

def get_website_info(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the title
    title = soup.title.string if soup.title else 'No title found'

    # Extract all headings (h1, h2, h3, etc.)
    headings = []
    for level in range(1, 7):  # h1 to h6
        for heading in soup.find_all(f'h{level}'):
            headings.append(heading.text.strip())

    return title, headings

def calculate_cosine_similarity(query, title, headings):
    # Combine the query, title, and headings into a single list
    documents = [query, title] + headings

    # Use TfidfVectorizer to convert the text to vectors
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between the query and the title/headings
    query_vector = vectors[0]  # First vector is the query
    title_vector = vectors[1]  # Second vector is the title
    heading_vectors = vectors[2:]  # Remaining vectors are the headings

    # Calculate similarities
    title_similarity = cosine_similarity([query_vector], [title_vector]).flatten()[0]
    heading_similarities = cosine_similarity([query_vector], heading_vectors).flatten()

    return title_similarity, heading_similarities

def seo_grading(html_content, base_url, query=None):
    title, headings = get_website_info(html_content)
    query = query if query else title
    title_similarity, heading_similarities = calculate_cosine_similarity(query, title, headings)
    robots_txt_status = check_robots_txt(base_url)

    return {
        "query": query,
        "title_similarity": title_similarity,
        "heading_similarities": {f"heading_{i+1}": similarity for i, similarity in enumerate(heading_similarities)},
        "robots_txt_status": robots_txt_status
    
    }
