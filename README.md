# AllTrails MCP Server
[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/srinath1510/alltrails-mcp-server)](https://archestra.ai/mcp-catalog/srinath1510__alltrails-mcp-server)

![CI](https://github.com/srinath1510/alltrails-mcp-server/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## ⚠️ DEPRECATED - PROJECT ARCHIVED

**This project has been deprecated and is no longer functional.**

**Date:** January 25, 2026  
**Reason:** This project violated AllTrails' Terms of Service by scraping their website without authorization.

At the request of AllTrails' CTO, all scraping functionality has been disabled. This repository is maintained for historical purposes only and to preserve GitHub stars, but **the code no longer works and should not be used**.

### What Happened?

AllTrails contacted me regarding this repository, citing:
- Unauthorized scraping/data extraction in violation of their Terms of Service
- Potential intellectual property violations
- Redistribution of copyrighted content without a license

### Alternatives

If you need trail data, please:
- Use [AllTrails' official website](https://www.alltrails.com/)
- Contact AllTrails directly about API access
- Respect website Terms of Service and copyright

---

## Original Description (For Historical Reference)

A Model Context Protocol (MCP) server that ~~provides access to AllTrails data~~ **[DEPRECATED - NO LONGER FUNCTIONAL]**.

## Features

- 🥾 **Search trails** by national park
- 📍 **Get detailed trail information** including difficulty, length, elevation gain, and descriptions
- 🏔️ **Comprehensive trail data** from AllTrails including ratings, route types, and summaries
- 🤖 **Seamless Client integration** via MCP protocol

## Technical Specifications

### Protocol Support

- **Protocol Version**: MCP 1.9.4
- **Communication**: Standard input/output (stdio)
- **Capabilities**: Tools
- **Server Name**: alltrails-mcp
- **Server Version**: 0.1.0

## Tools Available

### `search_trails`
Search for trails in a specific national park using AllTrails data.

**Parameters:**
- `park` (required): Park slug in format `us/state/park-name` (e.g., `us/tennessee/great-smoky-mountains-national-park`)

### `get_trail_details`
Get detailed information about a specific trail by its AllTrails slug.

**Parameters:**
- `slug` (required): Trail slug from AllTrails URL (the part after `/trail/`)

## Installation Options

### Option 1: With Virtual Environment (Recommended)

This approach isolates dependencies and prevents conflicts with other Python projects.

### 1. Clone the Repository

```
git clone <your-repo-url>
cd alltrails_mcp
```

### 2. Create Virtual Environment

```
python3 -m venv alltrails_mcp_venv
source alltrails_mcp_venv/bin/activate  # On Windows: alltrails_mcp_venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Verify Installation

Test that the server starts without errors:

```
python3 server.py
```

You should see the server start without crashing. Press Ctrl+C to stop.

## Prerequisites

- Python 3.8 or higher
- This server can be used with any MCP-compatible client. I use Claude Desktop with Pro subscription.
- macOS (tested) or other Unix-like system

---

### Option 2: With System Python

If you prefer not to use a virtual environment, you can install dependencies globally.

### 1. Clone the Repository

```
git clone <your-repo-url>
cd alltrails_mcp
```

### 2. Install Dependencies Globally

```
pip install -r requirements.txt
```

### 3. Verify Installation

Test that the server starts without errors:

```
python3 server.py
```

You should see the server start without crashing. Press Ctrl+C to stop.

---

### Option 3: With Docker

This approach runs the server in an isolated container.

#### 1. Build the Image

```bash
docker build -t alltrails-mcp .
```

#### 2. Run the Container

```bash
docker run -i --rm alltrails-mcp
```

#### 3. Use with Claude Desktop

For Docker-based deployment, you can configure Claude Desktop to use the containerized server:

```json
{
  "mcpServers": {
    "alltrails_mcp_server": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "alltrails-mcp"]
    }
  }
}
```

## Claude Desktop Configuration

### 1. Locate Claude Desktop Config

Find your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

If it doesn't exist, create a json file named claude_desktop_config.json in the above directory.

### 2. Add MCP Server Configuration

Add the following to your `claude_desktop_config.json` file:

#### Option A: Using Virtual Environment (Recommended)
```json
{
  "mcpServers": {
    "alltrails_mcp_server": {
      "command": "/path/to/your/alltrails_mcp/alltrails_mcp_venv/bin/python3",
      "args": ["/path/to/your/alltrails_mcp/server.py"]
    }
  }
}
```

#### Option B: Using System Python
```json
{
  "mcpServers": {
    "alltrails_mcp_server": {
      "command": "python3",
      "args": ["/path/to/your/alltrails_mcp/server.py"]
    }
  }
}
```

**Or with absolute Python path:**
```json
{
  "mcpServers": {
    "alltrails_mcp_server": {
      "command": "/usr/bin/python3",
      "args": ["/path/to/your/alltrails_mcp/server.py"]
    }
  }
}
```

**Important:** Replace `/path/to/your/alltrails_mcp` with the actual absolute path to your project directory.

#### Other MCP Clients

For other MCP-compatible clients, refer to their documentation for server configuration. The server implements the standard MCP protocol and should work with any compliant client.

**Server Command:** `python3 server.py`  
**Communication:** Standard input/output (stdio)  
**Protocol Version:** MCP 1.9.4

### 3. Find Your Python Path

#### For Virtual Environment Users:
```
cd /path/to/your/alltrails_mcp
source alltrails_mcp_venv/bin/activate
which python3
```

#### For System Python Users:
```
which python3
```

Use the output path in your configuration.

### 4. Install Dependencies

#### If Using Virtual Environment:
Dependencies are already installed in your virtual environment from step 3.

#### If Using System Python:
Install dependencies globally:
```
pip install -r requirements.txt
```

### 5. Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect.

## Usage Examples

Once configured, you can use these commands in Claude Desktop:

### Search for Trails

**By park name:**
```
Find trails in Great Smoky Mountains National Park
```

**By location:**
```
What are the best hiking trails in Yosemite?
```

**With specific criteria:**
```
Show me moderate difficulty trails in Yellowstone
```

**Using park slugs directly:**
```
Search for trails in us/california/yosemite-national-park
```

**For specific activities:**
```
Find family-friendly trails in Zion National Park
```

### Get Trail Details

**By trail name:**
```
Get details for Alum Cave Trail to Mount LeConte
```

**Using trail slugs:**
```
Get details for trail us/tennessee/alum-cave-trail-to-mount-leconte
```

**For planning purposes:**
```
I need detailed information about Rainbow Falls Trail including difficulty and elevation
```

### Combination Queries

**Search and get details:**
```
Find the most popular trails in Grand Canyon National Park and give me details about the top rated one
```

**Compare trails:**
```
Search for trails in Great Smoky Mountains and tell me which ones are best for beginners
```

**Trip planning:**
```
I'm visiting Yellowstone for 3 days. Find me a mix of easy and moderate trails with good views
```

### Natural Language Examples

The MCP server works with natural language, so you can ask questions like:

- "What are some good day hikes in the Smoky Mountains?"
- "Find me a challenging trail with waterfalls in Tennessee"
- "I want to hike to a summit with 360-degree views"
- "Show me trails that are good for photography"
- "Find dog-friendly trails in national parks"
- "What's the difficulty level of Charlies Bunion trail?"

### Common Park Slugs
- Great Smoky Mountains: `us/tennessee/great-smoky-mountains-national-park`
- Yosemite: `us/california/yosemite-national-park`
- Yellowstone: `us/wyoming/yellowstone-national-park`
- Grand Canyon: `us/arizona/grand-canyon-national-park`
- Zion: `us/utah/zion-national-park`

## Troubleshooting

### Server Not Connecting

1. **Check the logs:**
   ```bash
   tail -f ~/Library/Logs/Claude/mcp.log
   ```

2. **Verify your config file:**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Test the server manually:**
   ```bash
   cd /path/to/your/alltrails_mcp
   source alltrails_mcp_venv/bin/activate
   python3 server.py
   ```

### Common Issues

- **"Connection closed" errors**: Usually indicates a Python path or virtual environment issue
### **Path configuration issues**: Check that all paths in the config are absolute and correct
- **Import errors**: Ensure all dependencies are installed in the correct Python environment (virtual environment vs system Python)
- **Python path errors**: Use `which python3` or `which python` to verify the correct Python executable path

### Debug Mode

For detailed debugging, check the MCP logs:

```
# macOS
tail -f ~/Library/Logs/Claude/mcp.log

# The server also outputs debug information to stderr
```

## Development

### Running Tests

Run the test suite using pytest:

```bash
pytest
```

### Linting

Format and check code using ruff:

```bash
ruff check .
ruff format .
```

## Project Structure

```
alltrails_mcp/
├── app/
│   └── alltrails_scraper.py    # AllTrails scraping logic
├── examples/
│   └── claude_desktop_config.json  # Example configuration file for Claude Desktop
├── tests/                      # Test suite
│   ├── conftest.py             # Test fixtures
│   └── test_scraper.py         # Scraper tests
├── server.py                   # MCP server implementation
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration (Ruff, Pytest)
├── alltrails_mcp_venv/         # Virtual environment
├── README.md                   # This file
└── .gitignore                  # Git ignore file
```

## How It Works

1. **MCP Protocol**: Uses the Model Context Protocol to communicate with Claude Desktop
2. **Web Scraping**: Scrapes AllTrails website for trail data using BeautifulSoup
3. **Data Processing**: Formats and returns trail information in a structured format
4. **Tool Integration**: Exposes tools that Claude can call to search and retrieve trail data


## License

MIT License

Copyright (c) 2025 Srinath Srinivasan

## Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Trail data sourced from [AllTrails](https://www.alltrails.com/)
- Inspired by the MCP community examples

---

## ⚠️ IMPORTANT NOTICE

**This project is DEPRECATED and non-functional as of January 25, 2026.**

The scraping functionality violated AllTrails' Terms of Service and has been completely disabled at their request. This repository exists only for historical/educational purposes.

**DO NOT attempt to use, fork, or replicate this code for scraping AllTrails or any other website without explicit written permission from the website owner.**

Respect Terms of Service. Respect copyright. Use official APIs when available.