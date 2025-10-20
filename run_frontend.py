#!/usr/bin/env python3
"""
Starter script for Next.js frontend
"""

import subprocess
import sys
import os

def main():
    """Run the Next.js frontend"""
    # Change to the frontend directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(script_dir, "frontend")
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not os.path.exists("node_modules"):
        print("Installing dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)
    
    # Run Next.js dev server
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except subprocess.CalledProcessError as e:
        print(f"Error running Next.js: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
