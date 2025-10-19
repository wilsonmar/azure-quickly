#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "flask",
#   "markdown",
#   "requests",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file


"""mcp-ms-learn.py here.

at https://github.com/wilsonmar/azure-quickly/blob/main/mcp-ms-learn.py
by Wilson Mar

Query a MCP Server containing Microsoft's LEARN documents using
MCP-standard JSON 2.0 async protocol containing SSE (Server-Sent Event) text/event-streams.
Output to a JSON file converted to Markdown (.md) format, then HTML and
displayed by a Werkzeug localhost to the default internet browser.

USAGE:
    # cd azure-quickly
    chmod +x mcp-ms-learn.py
    run check mcp-ms-learn.py
    # See https://wilsonmar.github.io/mcp
    uv run mcp-ms-learn.py -v -q "Who is the CEO"

"""

#### SECTION 01. Metadata about this program file:

__last_commit__ = "25-10-18 v004 + query :mcp-ms-learn.py"
__status__      = "works until localhost has to be shutdown on macOS Sequoia 15.3.1"
# TODO: argparse query text.

#### SECTION 02: Import internal libraries already built-in into Python:

import argparse
from threading import Timer
import webbrowser
from typing import Dict, Any
import socket

import platform
import subprocess

#### SECTION 03: Import external libraries from PiPy:

try:
    from flask import Flask, render_template_string, request
    import json
    import markdown
    from pathlib import Path
    import requests
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  uv env env\n  source .venv/bin/activate")
    exit(9)

#### SECTION 04: Define hard-coded values in global variables:

test_run_endpoint = False
show_tools = False
mcp_server_url = "https://learn.microsoft.com/api/mcp"
query = "What is the difference between MCP and A2A?"
output_json_filepath = "mcp-ms-learn.json"
output_md_filepath = "mcp-ms-learn.md"

#### SECTION 05: parse inputs as arguments to command:

#import argparse
#from argparse import ArgumentParser
parser = argparse.ArgumentParser(allow_abbrev=True,description="secrets-utils.py")
#parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
parser.add_argument("-v", "--verbose", action="store_true", help="Show tools")
#parser.add_argument("-vv", "--debug", action="store_true", help="Debug outputs from functions")
#parser.add_argument("-s", "--summary", action="store_true", help="Show summary stats")

parser.add_argument("-q", "--query", type=str, help="Query for Microsoft answer")
parser.add_argument("-p", "--port", type=str, help="Port for localhost")
# Default -h = --help (list arguments)

args = parser.parse_args()

if args.verbose:       # -v --verbose (flag)
    show_tools = True
if args.query:      # -q  --query "what to answer"
    query = args.query
if args.port:          # -p  --port
    my_port = args.port


def test_endpoint(url: str) -> bool:
    """Test if the endpoint exists and is reachable."""
    try:
        response = requests.get(url, timeout=10)
        print(f"GET {url} - Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False


def list_mcp_tools(url: str) -> Dict[str, Any]:
    """List available tools from the MCP server.
    
    Args:
        url: The MCP server endpoint URL
    Returns:
        The JSON response from the server
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Handle Server-Sent Events (SSE) format
        if response.headers.get('content-type') == 'text/event-stream':
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    json_data = line[6:]
                    try:
                        return json.loads(json_data)
                    
                    except json.JSONDecodeError as json_err:
                        return {"error": f"Invalid JSON in SSE data: {json_err}"}
            return {"error": "No data found in SSE response"}
        else:
            try:
                return response.json()
            except json.JSONDecodeError as json_err:
                return {"error": f"Invalid JSON response: {json_err}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def query_mcp_server(url: str, query: str) -> Dict[str, Any]:
    """Query an MCP server with a query (question).
    
    Args:
        url: The MCP server endpoint URL
        query: The query to ask
    Returns:
        The JSON response from the server
    """
    # MCP protocol typically uses JSON-RPC 2.0 format
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "microsoft_docs_search",
            "arguments": {
                "query": query
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Debug: Print response details
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        
        # Check if response is empty
        if not response.text.strip():
            return {"error": "Empty response from server"}
        
        # Handle Server-Sent Events (SSE) format
        if response.headers.get('content-type') == 'text/event-stream':
            # Parse SSE format
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    json_data = line[6:]  # Remove 'data: ' prefix
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError as json_err:
                        return {
                            "error": f"Invalid JSON in SSE data: {json_err}",
                            "sse_data": json_data
                        }
            return {"error": "No data found in SSE response"}
        else:
            # Try to parse regular JSON
            try:
                return response.json()
            except json.JSONDecodeError as json_err:
                return {
                    "error": f"Invalid JSON response: {json_err}",
                    "response_text": response.text,
                    "status_code": response.status_code
                }
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def pretty_format_response(response: Dict[str, Any]) -> str:
    """Format the MCP response in a readable way.
    
    Args:
        response: The response dictionary from the MCP server
    Returns:
        A nicely formatted string representation
    """
    # Check for errors
    if "error" in response:
        return f"❌ Error: {response['error']}"
    
    # Format the response
    formatted = "=" * 60 + "\n"
    formatted += "MCP SERVER RESPONSE\n"
    formatted += "=" * 60 + "\n\n"
    
    # Pretty print the JSON with indentation
    formatted += json.dumps(response, indent=2, ensure_ascii=False)
    
    formatted += "\n\n" + "=" * 60
    
    return formatted


def format_json_to_markdown(json_file_path: str, output_path: str) -> None:
    """Read a JSON file and convert it to Markdown formatted text."""
    path = Path(json_file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    # Read JSON file:
    with open(json_file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Write pretty-printed JSON to a new file:
    markdown_output = []
    if "result" in data and "content" in data["result"]:
        for item in data["result"]["content"]:
            if "text" in item:
                try:
                    # The 'text' field itself contains a JSON string
                    inner_content_list = json.loads(item["text"])
                    for inner_item in inner_content_list:
                        title = inner_item.get("title", "No Title")
                        content_text = inner_item.get("content", "No Content")
                        content_url = inner_item.get("contentUrl", "#")
                        markdown_output.append(f"## {title}\n\n{content_text}\n\n[Read more]({content_url})\n\n---\n")
                except json.JSONDecodeError:
                    markdown_output.append(f"## Raw Content\n\n{item['text']}\n\n---\n")

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(markdown_output) if markdown_output else "No parsable content found.")
    
    print(f"Markdown-formatted content written to: {output_path}")
    return

def is_port_available(port_in: int, host: str = '127.0.0.1') -> bool:
    """Check if a port is available.
    
    USAGE: if is_port_available(5000):
    """
    #import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port_in))
            return True  # Port is available
        except OSError:
            return False  # Port is already in use

def get_port_available(port_in: int, host: str = '127.0.0.1') -> bool:
    """Iterate through ports to find one available."""
    x = int(port_in)
    for port in range(x, x + 1):
        print(f"TRACE: get_port_available() trying port {port} at [X]")
        if is_port_available(port):
            return port


def get_default_browser():
    os_name = platform.system()

    # Windows: Query the registry
    if os_name == "Windows":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice") as key:
                prog_id, _ = winreg.QueryValueEx(key, "ProgId")
                return prog_id  # e.g. "ChromeHTML", "MSEdgeHTM", "FirefoxURL"
        except FileNotFoundError:
            return "Unknown (no default set)"

    # macOS: use Apple’s Launch Services
    elif os_name == "Darwin":
        try:
            result = subprocess.run(
                ["defaults", "read", "com.apple.LaunchServices/com.apple.launchservices.secure",
                 "LSHandlers"],
                capture_output=True, text=True
            )
            if ".https" in result.stdout:
                if "Safari" in result.stdout:
                    return "Safari"
                elif "Chrome" in result.stdout:
                    return "Chrome"
                elif "Firefox" in result.stdout:
                    return "Firefox"
            return "Unknown"
        except Exception:
            return "Unknown"

    # Linux: use xdg-settings or fallback
    elif os_name == "Linux":
        try:
            browser = subprocess.run(
                ["xdg-settings", "get", "default-web-browser"],
                capture_output=True, text=True
            )
            return browser.stdout.strip()
        except Exception:
            return "Unknown"

    return "Unsupported OS"


app = Flask(__name__)
@app.route('/')  # referenced by function index()
def index():
    """Display markdown (md) file as html in browser."""
    # Open file and read it into "md_content"
    if not output_md_filepath:
        print("FAIL: no md_filepath specified!")
        return "Error: No markdown file specified"
    
    with open(output_md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # Convert Markdown to HTML using the markdown package:
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
    # Basic HTML wrapper:
    html_page = f"""
    <html>
        <head><title>Markdown Preview</title></head>
        <body>{html_content}</body>
    </html>
    """
    # Serve the HTML result using Flask:
    print("INFO: File is accessible at http://localhost:5000/")
    return render_template_string(html_page)


def open_browser(port="5000"):
    """Open browser using a delay."""
    webbrowser.open_new(f"http://127.0.0.1:{port}")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/down', methods=['GET'])
def shutdown():
    """Shutdown server with url http://localhost:5000/down browser address."""
    shutdown_server()
    return 'Server shutting down...'

def main():
    """Just do the program."""
    if mcp_server_url:
        print(f"Querying MCP server at: {mcp_server_url}")
    else:
        print("FAIL: No mcp_server_url!")
        exit(9)
    
    if test_run_endpoint:
        print(f"Testing endpoint: {mcp_server_url}")
        if not test_endpoint(mcp_server_url):
            print("\n⚠️  The endpoint might not exist. Trying MCP request anyway...\n")
    
    if show_tools:
        print(f"Listing available tools from: {mcp_server_url}")
        tools_response = list_mcp_tools(mcp_server_url)
        print("Available tools:")
        print(json.dumps(tools_response, indent=2))
        print("\n" + "="*60 + "\n")
    
    if not query:
        print("FAIL: No query text to answer!")
        exit(9)
    # else:

    print(f"Query: {query}\n")
    # Query the server
    response = query_mcp_server(mcp_server_url, query)

    # Pretty format and display the response
    formatted_output = pretty_format_response(response)
    print(formatted_output)
    
    # Optionally save to file
    with open(output_json_filepath, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Response saved to: {output_json_filepath}")

    format_json_to_markdown(output_json_filepath, output_md_filepath)

    print("INFO: Default browser:", get_default_browser())

    # if md file exists:
    # Open the browser after the specified number of seconds of delay:
    Timer(2, open_browser).start()

    use_port = get_port_available(my_port)
    app.run(debug=False,port=use_port)
    # TODO: Because app.run() is blocking, Flask’s built-in server doesn’t natively support stopping the server automatically right after app.run() starts (without external request).
    # You’d need to run the server in a separate thread or process and then 
    # kill it programmatically using signals (os.kill) or similar methods, which  
    # is more complex and less clean.

if __name__ == "__main__":
    main()
