#!/usr/bin/env python3
"""
AllTrails MCP Server - FastMCP compatible version
"""

from fastmcp import FastMCP
from app.alltrails_scraper import search_trails_in_park, get_trail_by_slug
import sys

# Initialize FastMCP server
mcp = FastMCP("alltrails-mcp", version="0.1.0")

@mcp.tool()
def search_trails(park: str) -> str:
    """
    Search for trails in a specific national park using AllTrails data.
    
    Args:
        park: Park slug in format 'us/state/park-name' (e.g., 'us/tennessee/great-smoky-mountains-national-park')
    
    Returns:
        A formatted list of trails found in the specified park
    """
    try:
        print(f"Searching trails for park: {park}", file=sys.stderr)
        trails = search_trails_in_park(park)
        
        if not trails:
            return f"No trails found for park: {park}. Please check the park slug format."
        
        response = f"Found {len(trails)} trails in {park}:\n\n"
        for i, trail in enumerate(trails[:15], 1):  # Limit to top 15 trails
            response += f"{i}. **{trail['name']}**\n"
            if trail.get('difficulty'):
                response += f"   - Difficulty: {trail['difficulty']}\n"
            if trail.get('length'):
                response += f"   - Length: {trail['length']}\n"
            if trail.get('rating'):
                response += f"   - Rating: {trail['rating']}\n"
            if trail.get('summary'):
                summary = trail['summary'][:80] + "..." if len(trail['summary']) > 80 else trail['summary']
                response += f"   - Summary: {summary}\n"
            response += f"   - URL: {trail['url']}\n\n"
        
        if len(trails) > 15:
            response += f"... and {len(trails) - 15} more trails."
        
        return response
    except Exception as e:
        print(f"Error in search_trails: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return f"Error searching trails: {str(e)}"

@mcp.tool()
def get_trail_details(slug: str) -> str:
    """
    Get detailed information about a specific trail by its AllTrails slug.
    
    Args:
        slug: Trail slug from AllTrails URL (the part after '/trail/')
    
    Returns:
        Detailed information about the specified trail
    """
    try:
        print(f"Getting trail details for: {slug}", file=sys.stderr)
        trail = get_trail_by_slug(slug)
        
        if not trail or not trail.get('title'):
            return f"Trail not found for slug: {slug}. Please check the trail slug."
        
        # Format detailed trail information
        response = f"# {trail['title']}\n\n"
        if trail.get('length'):
            response += f"**Length:** {trail['length']}\n"
        if trail.get('elevation_gain'):
            response += f"**Elevation Gain:** {trail['elevation_gain']}\n"
        if trail.get('route_type'):
            response += f"**Route Type:** {trail['route_type']}\n"
        if trail.get('difficulty'):
            response += f"**Difficulty:** {trail['difficulty']}\n"
        if trail.get('rating'):
            response += f"**Rating:** {trail['rating']}\n"
        response += f"**URL:** {trail['url']}\n\n"
        
        if trail.get('summary'):
            response += f"**Description:**\n{trail['summary']}\n"
        
        return response
    except Exception as e:
        print(f"Error in get_trail_details: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return f"Error getting trail details: {str(e)}"