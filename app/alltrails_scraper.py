# ============================================================================
# DEPRECATED - THIS CODE HAS BEEN DISABLED
# ============================================================================
# This file previously contained web scraping functionality for AllTrails.
# The code has been disabled in compliance with AllTrails' Terms of Service.
# 
# Date Deprecated: January 25, 2026
# Reason: Violation of AllTrails ToS - unauthorized scraping/data extraction
# 
# This repository is maintained for historical/educational purposes only.
# DO NOT USE THIS CODE TO SCRAPE ALLTRAILS OR ANY OTHER WEBSITE WITHOUT
# EXPLICIT PERMISSION FROM THE WEBSITE OWNER.
# ============================================================================

"""
DEPRECATED MODULE - DO NOT USE

This module previously scraped AllTrails data, which violated their Terms of Service.
All functionality has been disabled.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# All scraping functionality has been removed to comply with AllTrails ToS


def search_trails_in_park(park_slug: str) -> List[Dict]:
    """
    DEPRECATED - This function has been disabled.
    
    This function previously scraped AllTrails data, which violated their ToS.
    """
    logger.error("This functionality has been deprecated and disabled.")
    raise NotImplementedError(
        "This MCP server has been deprecated due to Terms of Service violations. "
        "Please use AllTrails' official API or website directly."
    )


def get_trail_by_slug(slug: str) -> Dict:
    """
    DEPRECATED - This function has been disabled.
    
    This function previously scraped AllTrails data, which violated their ToS.
    """
    logger.error("This functionality has been deprecated and disabled.")
    raise NotImplementedError(
        "This MCP server has been deprecated due to Terms of Service violations. "
        "Please use AllTrails' official API or website directly."
    )


# ============================================================================
# ORIGINAL CODE ARCHIVED BELOW (COMMENTED OUT)
# ============================================================================
# The original implementation has been commented out to preserve the repository
# structure while complying with AllTrails' request to disable scraping.
# ============================================================================

"""
# Original imports (DISABLED)
import re
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.alltrails.com"

# ... (rest of original code commented out)
# See git history for full original implementation
"""
