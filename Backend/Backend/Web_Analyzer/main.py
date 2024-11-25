from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from database import ScrapedContent, get_db
from colorgrading import color_grading
from scraper import (find_properties, extract_css_from_webpage)
import requests
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from typing import Optional
from fastapi.staticfiles import StaticFiles
from content_style_grading import check_consistency, font_harmony
from ads_recommendation import recommend_ads
from ads_data import ad_topic_mapping
from responsive import responsive
from Seo_grading import seo_grading
from web_security import scrape_payment_elements, review_http_headers, inspect_cookies_and_tokens, analyze_session_management, authorization_checks
from methods import (run_link_checker, fetch_webpage, parse_html, extract_css_js_files, evaluate_file_sizes)
from database import SessionLocal, engine, get_db, Base, User, Report
from passlib.context import CryptContext
import shutil
import os
import base64
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ScrapeRequest(BaseModel):
    url: str
    feature: Optional[str] = None
    sub_feature: Optional[str] = None
    query: Optional[str] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    user_details: str
    sub_details: str
    profession: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    user_details: str = Form(...),
    sub_details: str = Form(...),
    profession: str = Form(...),
    image: UploadFile = File(None),  # Optional file
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        username=username,
        password=hashed_password,
        user_details=user_details,
        sub_details=sub_details,
        profession=profession
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Save user image
    if image:
        image_path = f"static/{new_user.user_id}.jpg"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    return {"message": "User registered successfully", "user_id": new_user.user_id}

@app.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "user_details": user.user_details,
        "sub_details": user.sub_details,
        "profession": user.profession,
        "days_left": user.days_left,
        "created_at": user.created_at,
        "image": f"/static/{user.user_id}.jpg"
    }

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "user_details": user.user_details,
        "sub_details": user.sub_details,
        "profession": user.profession,
        "days_left": user.days_left,
        "created_at": user.created_at,
        "image": f"/static/{user.user_id}.jpg"
    }
    

class ReportRequest(BaseModel):
    user_id: int
    feature: str
    sub_feature: str
    data: dict

@app.post("/save_report")
async def save_report(report_request: ReportRequest, db: Session = Depends(get_db)):
    new_report = Report(
        user_id=report_request.user_id,
        feature=report_request.feature,
        sub_feature=report_request.sub_feature,
        data=report_request.data
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return {"message": "Report saved successfully", "report_id": new_report.report_id}

@app.get("/reports/{user_id}")
def get_reports(user_id: int, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")
    return reports


class Scraper:
    def __init__(self, url, db: Session):
        self.url = url
        self.db = db
        self.html_elements = ""
        self.elements_properties = {}
        self.css = ""
        self.body_content = ""

    def fetch_and_parse(self):
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        self.body_content = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
        self.html_elements = str(soup)
        self.css = extract_css_from_webpage(self.url)
        
        # Convert to a Python dictionary if find_properties returns a JSON string
        print(1)
        properties = find_properties(self.url, [
            'background-color', 'color', 'font-family', 'font-size', 'font-weight',
            'margin', 'padding', 'text-align', 'justify-content', 'align-items'
        ])
        print(2)
        
        if isinstance(properties, str):  # If properties is a JSON string, convert it
            print(3)
            self.elements_properties = json.loads(properties)
        else:
            print(4)
            self.elements_properties = properties

    def save_to_db(self):
        # Print the type and value of elements_properties and css before serialization
        print("Before serialization:")
        print(f"Type of elements_properties: {type(self.elements_properties)}")
        print(f"Value of elements_properties: {self.elements_properties}")
        print(f"Type of css: {type(self.css)}")
        print(f"Value of css: {self.css}")

        # Serialize if needed
        elements_properties_serialized = json.dumps(self.elements_properties) if isinstance(self.elements_properties, dict) else self.elements_properties
        css_serialized = json.dumps(self.css) if isinstance(self.css, (list, tuple)) else self.css

        # Print the type and value of elements_properties and css after serialization
        print("After serialization:")
        print(f"Type of elements_properties_serialized: {type(elements_properties_serialized)}")
        print(f"Value of elements_properties_serialized: {elements_properties_serialized}")
        print(f"Type of css_serialized: {type(css_serialized)}")
        print(f"Value of css_serialized: {css_serialized}")

        # Create the ScrapedContent object
        scraped_content = ScrapedContent(
            url=self.url,
            html_elements=self.html_elements,
            elements_properties=elements_properties_serialized,  # JSON serialization here
            css=css_serialized,  # Serialize tuple or list
            body_content=self.body_content,
            created_at=datetime.datetime.utcnow()
        )

        # Add to the session
        self.db.add(scraped_content)

        try:
            # Commit the transaction
            self.db.commit()
            # Refresh to get the updated instance (ID and other auto-generated fields)
            self.db.refresh(scraped_content)
        except Exception as e:
            # Rollback in case of error
            self.db.rollback()
            raise ValueError(f"Error during commit: {e}")





    def load_from_db(self):
        return self.db.query(ScrapedContent).filter(ScrapedContent.url == self.url).first()

@app.post("/scrape")
async def scrape(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if existing_content:
            return {
                "message": "Content already exists in the database.",
                "data": existing_content
            }
        else:
            print(10)
            scraper.fetch_and_parse()
            print(11)
            scraper.save_to_db()
            print(12)
            return {
                "message": "Content scraped and saved successfully.",
                "data": {
                    "url": scraper.url,
                    "html_elements": scraper.html_elements,
                    "elements_properties": scraper.elements_properties,
                    "css": scraper.css,
                    "body_content": scraper.body_content
                }
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_html_content(db: Session, url: str):
    scraped_content = db.query(ScrapedContent).filter(ScrapedContent.url == url).first()
    if not scraped_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return scraped_content.html_elements

@app.post("/consistency")
async def consistency_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        html_content = existing_content.html_elements
        consistency_report = check_consistency(html_content)
        return {
            "message": "Consistency analysis completed successfully.",
            "report": consistency_report
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/color_grading")
async def color_grading_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        elements_properties = json.loads(existing_content.elements_properties)
        grading_results = color_grading(elements_properties)
        return {
            "message": "Color grading calculated successfully.",
            "results": grading_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/font_harmony")
async def font_harmony_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve elements properties from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }

        elements_properties = json.loads(existing_content.elements_properties)  # Ensure it's parsed to dict

        harmony_results = font_harmony(elements_properties)

        return {
            "message": "Font harmony analysis completed successfully.",
            "results": harmony_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/check_links")
async def check_links(scrape_request: ScrapeRequest):
    links_report = run_link_checker(scrape_request.url)
    return {"message": "Link checking completed", "details": links_report}

@app.post("/evaluate_files")
async def evaluate_files(scrape_request: ScrapeRequest):
    html_content = fetch_webpage(scrape_request.url)
    if html_content:
        soup = parse_html(html_content)
        css_files, js_files, internal_css, internal_js = extract_css_js_files(soup, scrape_request.url)
        total_css_size, total_js_size = evaluate_file_sizes(css_files, js_files, internal_css, internal_js)
        return {
            "total_css_size_kb": total_css_size / 1024,
            "total_js_size_kb": total_js_size / 1024
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch the webpage")
    
@app.post("/responsive")
async def responsive_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve HTML and CSS from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }

        html_content = existing_content.html_elements
        css_content = [existing_content.css]  # Assuming css is a single string, if not modify accordingly

        # Calculate responsive design score
        responsive_results = responsive(html_content, css_content)

        return {
            "message": "Responsive design analysis completed successfully.",
            "results": responsive_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/seo_grading")
async def seo_grading_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve html_content and css from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        
        html_content = existing_content.html_elements
        base_url = scraper.url

        # Perform SEO grading
        seo_results = seo_grading(html_content, base_url, scrape_request.query)

        return {
            "message": "SEO grading completed successfully.",
            "results": seo_results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.post("/web_security")
async def web_security_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve html_content from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        
        html_content = existing_content.html_elements
        base_url = scraper.url
        
        # Perform web security analysis
        security_results = scrape_payment_elements(html_content, base_url)
        
        with requests.Session() as session:
            # Assuming you have login details and a protected URL for testing
            username = "your_username"
            password = "your_password"
            login_url = f"{base_url}/login"
            protected_url = f"{base_url}/protected"
            
            cookie_token_results = inspect_cookies_and_tokens(session, login_url, username, password)
            session_management_results = analyze_session_management(session)
            authorization_results = authorization_checks(session, protected_url)
            
            response = requests.get(base_url)
            header_results = review_http_headers(response)
        
        return {
            "message": "Web security analysis completed successfully.",
            "results": {
                "payment_security": security_results,
                "cookie_and_token_inspection": cookie_token_results,
                "session_management": session_management_results,
                "authorization_checks": authorization_results,
                "http_headers": header_results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/ads_recommendation")
async def ads_recommendation_endpoint(scrape_request: ScrapeRequest, db: Session = Depends(get_db)):
    try:
        # Retrieve body_content from the database
        scraper = Scraper(scrape_request.url, db)
        existing_content = scraper.load_from_db()
        if not existing_content:
            return {
                "message": "Content not found in the database."
            }
        
        body_content = existing_content.body_content

        # Perform ads recommendation
        ad_topics = recommend_ads(body_content, ad_topic_mapping)

        return {
            "message": "Ads recommendation completed successfully.",
            "results": ad_topics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
