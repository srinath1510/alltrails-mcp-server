import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)

BASE_URL = "https://www.alltrails.com"

def get_headers():
    """Get headers for web scraping to avoid being blocked."""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

def extract_distance_and_rating(text: str) -> tuple[Optional[str], Optional[str]]:
    """Extract distance and rating from trail card text."""
    distance = None
    rating = None
    
    # Look for distance pattern (e.g., "2.4 mi", "5.1 km")
    distance_match = re.search(r'(\d+\.?\d*)\s*(mi|km)', text)
    if distance_match:
        distance = distance_match.group(0)
    
    # Look for rating pattern (e.g., "4.5", "3.8")
    rating_match = re.search(r'(\d+\.?\d*)\s*(?:stars?|★)', text)
    if rating_match:
        rating = rating_match.group(1)
    
    return distance, rating

def search_trails_in_park(park_slug: str) -> List[Dict]:
    """
    Search for trails in a specific park.
    
    Args:
        park_slug: Park identifier (e.g., 'us/tennessee/great-smoky-mountains-national-park')
    
    Returns:
        List of trail dictionaries with name, url, summary, difficulty, etc.
    """
    url = f"{BASE_URL}/parks/{park_slug}"
    
    try:
        logger.info(f"Fetching trails from: {url}")
        resp = requests.get(url, headers=get_headers(), timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        trails = []
        
        # Try multiple selectors for trail cards as AllTrails may update their HTML
        card_selectors = [
            "div[data-testid='trail-card']",
            "div.trail-card",
            "a[data-testid='trail-card-title-link']",
            ".styles-module__container___3ZXxx"
        ]
        
        cards = []
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                logger.info(f"Found {len(cards)} trail cards using selector: {selector}")
                break
        
        if not cards:
            # Try to find any links that look like trails
            trail_links = soup.find_all("a", href=re.compile(r"/trail/"))
            logger.info(f"Found {len(trail_links)} trail links as fallback")
            
            for link in trail_links[:20]:  # Limit to prevent too many results
                name = link.get_text(strip=True)
                if name and len(name) > 3:  # Filter out very short names
                    trail_url = BASE_URL + link["href"] if link["href"].startswith("/") else link["href"]
                    trails.append({
                        "name": name,
                        "url": trail_url,
                        "summary": "",
                        "difficulty": "",
                        "length": "",
                        "rating": ""
                    })
            
            return trails
        
        # Process trail cards
        for card in cards:
            try:
                # Try different methods to extract trail information
                name_elem = (
                    card.find("a", {"data-testid": "trail-card-title-link"}) or
                    card.find("h3") or
                    card.find("a", href=re.compile(r"/trail/")) or
                    card.find("span", class_=re.compile(r"name|title", re.I))
                )
                
                if not name_elem:
                    continue
                
                name = name_elem.get_text(strip=True)
                if not name:
                    continue
                
                # Get trail URL
                trail_url = None
                if name_elem.name == "a" and name_elem.get("href"):
                    trail_url = BASE_URL + name_elem["href"] if name_elem["href"].startswith("/") else name_elem["href"]
                else:
                    # Look for any link in the card
                    link_elem = card.find("a", href=re.compile(r"/trail/"))
                    if link_elem:
                        trail_url = BASE_URL + link_elem["href"] if link_elem["href"].startswith("/") else link_elem["href"]
                
                if not trail_url:
                    continue
                
                # Extract difficulty
                difficulty_elem = (
                    card.find("span", class_=re.compile(r"difficulty", re.I)) or
                    card.find("div", class_=re.compile(r"difficulty", re.I)) or
                    card.find(text=re.compile(r"Easy|Moderate|Hard", re.I))
                )
                difficulty = difficulty_elem.get_text(strip=True) if hasattr(difficulty_elem, 'get_text') else str(difficulty_elem).strip() if difficulty_elem else ""
                
                # Extract summary/description
                summary_selectors = [
                    "div.styles-module__text___1Jt3Z",
                    "p[data-testid='trail-card-description']",
                    ".trail-description",
                    "p"
                ]
                
                summary = ""
                for selector in summary_selectors:
                    summary_elem = card.select_one(selector)
                    if summary_elem:
                        summary = summary_elem.get_text(strip=True)
                        if len(summary) > 20:  # Only use if it's substantial
                            break
                
                # Try to extract length and rating from card text
                card_text = card.get_text()
                length, rating = extract_distance_and_rating(card_text)
                
                trail_data = {
                    "name": name,
                    "url": trail_url,
                    "summary": summary,
                    "difficulty": difficulty,
                    "length": length or "",
                    "rating": rating or ""
                }
                
                trails.append(trail_data)
                
            except Exception as e:
                logger.warning(f"Error processing trail card: {e}")
                continue
        
        logger.info(f"Successfully extracted {len(trails)} trails")
        return trails
        
    except requests.RequestException as e:
        logger.error(f"Request error when fetching {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error when parsing trails: {e}")
        return []

def get_trail_by_slug(slug: str) -> Dict:
    """
    Get detailed information about a specific trail.
    
    Args:
        slug: Trail slug from AllTrails URL
    
    Returns:
        Dictionary with detailed trail information
    """
    url = f"{BASE_URL}/trail/{slug}"
    
    try:
        logger.info(f"Fetching trail details from: {url}")
        resp = requests.get(url, headers=get_headers(), timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Extract title
        title_selectors = [
            "h1[data-testid='trail-title']",
            "h1.styles-module__title___1BPJy",
            "h1",
            "[data-testid='trail-name']"
        ]
        
        title = None
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        # Extract summary/description
        summary_selectors = [
            "[data-testid='trail-description']",
            "div.styles-module__text___1Jt3Z",
            ".trail-description",
            "meta[name='description']"
        ]
        
        summary = ""
        for selector in summary_selectors:
            if selector.startswith("meta"):
                elem = soup.select_one(selector)
                if elem:
                    summary = elem.get("content", "")
                    break
            else:
                elem = soup.select_one(selector)
                if elem:
                    summary = elem.get_text(strip=True)
                    if len(summary) > 50:  # Only use substantial descriptions
                        break
        
        # Extract stats - try multiple approaches
        stats = {}
        
        # Method 1: Look for specific stat elements
        stat_selectors = [
            "[data-testid='trail-length']",
            "[data-testid='trail-elevation']",
            "[data-testid='trail-difficulty']",
            "span.css-1d3z3hw",
            ".trail-stats span"
        ]
        
        for selector in stat_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if "mi" in text or "km" in text:
                    stats["length"] = text
                elif "ft" in text or "m" in text and "gain" in text.lower():
                    stats["elevation_gain"] = text
        
        # Method 2: Look for structured data or specific patterns
        page_text = soup.get_text()
        
        # Extract length
        length_match = re.search(r'Length[:\s]*(\d+\.?\d*\s*(?:mi|km|miles|kilometers))', page_text, re.I)
        if length_match and "length" not in stats:
            stats["length"] = length_match.group(1)
        
        # Extract elevation gain
        elevation_match = re.search(r'Elevation[:\s]*(\d+\.?\d*\s*(?:ft|feet|m|meters))', page_text, re.I)
        if elevation_match and "elevation_gain" not in stats:
            stats["elevation_gain"] = elevation_match.group(1)
        
        # Extract difficulty
        difficulty_match = re.search(r'Difficulty[:\s]*(Easy|Moderate|Hard)', page_text, re.I)
        difficulty = difficulty_match.group(1) if difficulty_match else ""
        
        # Extract rating
        rating_selectors = [
            "[data-testid='trail-rating']",
            ".reviewRating",
            ".rating-display"
        ]
        
        rating = ""
        for selector in rating_selectors:
            rating_elem = soup.select_one(selector)
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    rating = rating_match.group(1)
                    break
        
        # Extract route type
        route_type = ""
        route_match = re.search(r'Route type[:\s]*(Out & back|Loop|Point to point)', page_text, re.I)
        if route_match:
            route_type = route_match.group(1)
        
        return {
            "title": title or f"Trail {slug}",
            "summary": summary,
            "length": stats.get("length", ""),
            "elevation_gain": stats.get("elevation_gain", ""),
            "route_type": route_type,
            "difficulty": difficulty,
            "rating": rating,
            "url": url,
            "stats": stats
        }
        
    except requests.RequestException as e:
        logger.error(f"Request error when fetching {url}: {e}")
        return {"title": "", "summary": f"Error fetching trail: {e}", "url": url}
    except Exception as e:
        logger.error(f"Unexpected error when parsing trail {slug}: {e}")
        return {"title": "", "summary": f"Error parsing trail: {e}", "url": url}