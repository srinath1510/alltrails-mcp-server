import asyncio
import sys
from datetime import datetime

print(f"{datetime.now()}: Starting AllTrails MCP server", file=sys.stderr)

try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    
    print("MCP imports successful", file=sys.stderr)
    
    # Import AllTrails scraper
    from app.alltrails_scraper import search_trails_in_park, get_trail_by_slug
    print("AllTrails scraper imports successful", file=sys.stderr)
    
    server = Server("alltrails-mcp")
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        print("list_tools called", file=sys.stderr)
        return [
            types.Tool(
                name="search_trails",
                description="Search for trails in a specific national park using AllTrails data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "park": {
                            "type": "string",
                            "description": "Park slug in format 'us/state/park-name' (e.g., 'us/tennessee/great-smoky-mountains-national-park')"
                        }
                    },
                    "required": ["park"]
                }
            ),
            types.Tool(
                name="get_trail_details",
                description="Get detailed information about a specific trail by its AllTrails slug",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slug": {
                            "type": "string",
                            "description": "Trail slug from AllTrails URL (the part after '/trail/')"
                        }
                    },
                    "required": ["slug"]
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        print(f"call_tool: {name} with {arguments}", file=sys.stderr)
        
        try:
            if name == "search_trails":
                park = arguments.get("park")
                if not park:
                    return [types.TextContent(type="text", text="Park parameter is required")]
                
                print(f"Searching trails for park: {park}", file=sys.stderr)
                trails = search_trails_in_park(park)
                
                if not trails:
                    return [types.TextContent(
                        type="text",
                        text=f"No trails found for park: {park}. Please check the park slug format."
                    )]
                
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
                
                return [types.TextContent(type="text", text=response)]
            
            elif name == "get_trail_details":
                slug = arguments.get("slug")
                if not slug:
                    return [types.TextContent(type="text", text="Slug parameter is required")]
                
                print(f"Getting trail details for: {slug}", file=sys.stderr)
                trail = get_trail_by_slug(slug)
                
                if not trail or not trail.get('title'):
                    return [types.TextContent(
                        type="text",
                        text=f"Trail not found for slug: {slug}. Please check the trail slug."
                    )]
                
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
                
                return [types.TextContent(type="text", text=response)]
            
            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
        
        except Exception as e:
            print(f"Error in tool {name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def main():
        print("Creating server capabilities", file=sys.stderr)
        
        capabilities = types.ServerCapabilities(
            tools=types.ToolsCapability(listChanged=False)
        )
        
        init_options = InitializationOptions(
            server_name="alltrails",
            server_version="0.1.0",
            capabilities=capabilities
        )
        
        print("Starting stdio server", file=sys.stderr)
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("AllTrails MCP server running", file=sys.stderr)
            await server.run(
                read_stream,
                write_stream,
                initialization_options=init_options
            )
    
    if __name__ == "__main__":
        asyncio.run(main())
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)