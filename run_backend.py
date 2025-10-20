#!/usr/bin/env python3
"""
Starter script for FastAPI backend
"""

import subprocess
import sys
import os

def main():
    """Run the FastAPI backend"""
    # Change to the backend directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(script_dir, "backend")
    os.chdir(backend_dir)
    
    # Run FastAPI with uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except subprocess.CalledProcessError as e:
        print(f"Error running FastAPI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
