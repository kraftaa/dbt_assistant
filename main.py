#!/usr/bin/env python3
"""
DBT Assistant - Main Entry Point

This script provides access to both the CLI and Flask app versions of the DBT Assistant.
"""

import sys
import os
from pathlib import Path

def main():
    """Main entry point for the DBT Assistant"""
    
    # Add app directory to path
    app_path = Path(__file__).parent / "app"
    sys.path.insert(0, str(app_path))
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ["cli", "command", "interactive"]:
            # Run CLI version
            from cli import main as cli_main
            cli_main()
        elif command in ["api", "server", "flask", "web"]:
            # Run Flask API server
            from app import app
            print("🚀 Starting DBT Assistant API server...")
            print("📡 API will be available at: http://localhost:5000")
            print("🔍 Search endpoint: http://localhost:5000/search")
            print("⏹️  Press Ctrl+C to stop the server")
            app.run(host="0.0.0.0", port=5000, debug=True)
        elif command in ["help", "--help", "-h"]:
            show_help()
        else:
            print(f"❌ Unknown command: {command}")
            show_help()
    else:
        # Default to CLI
        from cli import main as cli_main
        cli_main()

def show_help():
    """Show usage information"""
    print("""
🔎 DBT Assistant - AI-Powered Data Model Search

Usage:
  python main.py [command]

Commands:
  cli, command, interactive  Run interactive CLI (default)
  api, server, flask, web   Run Flask API server
  help, --help, -h         Show this help message

Examples:
  python main.py            # Run CLI (default)
  python main.py cli        # Run CLI explicitly
  python main.py api        # Start API server

For more information, see README.md
""")

if __name__ == "__main__":
    main()
