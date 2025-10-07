#!/usr/bin/env python3
"""
Setup script for Warhammer 40K Lore Assistant
This script helps set up the development environment and initial data collection
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed or not in PATH")
    print("Please install Node.js 18+ from https://nodejs.org/")
    return False

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    result = run_command("pip install -r requirements.txt", cwd=backend_dir)
    if result is None:
        print("❌ Failed to install Python dependencies")
        return False
    
    print("✅ Backend dependencies installed")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n🔧 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install Node.js dependencies
    print("Installing Node.js dependencies...")
    result = run_command("npm install", cwd=frontend_dir)
    if result is None:
        print("❌ Failed to install Node.js dependencies")
        return False
    
    print("✅ Frontend dependencies installed")
    return True

def create_env_file():
    """Create environment file from example"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    else:
        print("❌ env.example file not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "logs", "backend/data", "frontend/public"]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_initial_data_collection():
    """Run initial data collection"""
    print("\n📚 Running initial data collection...")
    print("This will scrape key Warhammer 40K pages from Lexicanum...")
    
    response = input("Do you want to run initial data collection? (y/N): ")
    if response.lower() != 'y':
        print("⏭️  Skipping initial data collection")
        return True
    
    # Run the data collection script
    script_path = Path("scripts/initial_data_collection.py")
    if script_path.exists():
        result = run_command(f"python {script_path}")
        if result is None:
            print("❌ Initial data collection failed")
            return False
        print("✅ Initial data collection completed")
    else:
        print("❌ Initial data collection script not found")
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Start the backend server:")
    print("   cd backend && uvicorn app.main:app --reload")
    print("3. Start the frontend (in a new terminal):")
    print("   cd frontend && npm start")
    print("4. Open http://localhost:3000 in your browser")
    print("\n🐳 Alternative: Use Docker Compose")
    print("   docker-compose up --build")
    print("\n📖 For more information, see README.md and DEPLOYMENT.md")

def main():
    """Main setup function"""
    print("🚀 Warhammer 40K Lore Assistant Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Set up backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Set up frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Run initial data collection (optional)
    run_initial_data_collection()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
