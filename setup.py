#!/usr/bin/env python3
"""
Setup script for Social Media Application
This script helps with initial project configuration and setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install Python dependencies"""
    # Determine the correct pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def run_migrations():
    """Run Django migrations"""
    # Determine the correct python command based on OS
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    success = True
    success &= run_command(f"{python_cmd} manage.py makemigrations", "Creating database migrations")
    success &= run_command(f"{python_cmd} manage.py migrate", "Applying database migrations")
    return success

def create_superuser():
    """Create a superuser account"""
    print("\nWould you like to create a superuser account? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes']:
        # Determine the correct python command based on OS
        if os.name == 'nt':  # Windows
            python_cmd = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS
            python_cmd = "venv/bin/python"
        
        return run_command(f"{python_cmd} manage.py createsuperuser", "Creating superuser account")
    
    print("Skipping superuser creation")
    return True

def main():
    """Main setup function"""
    print("=" * 50)
    print("Social Media Application Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\nFailed to create virtual environment. Please check your Python installation.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nFailed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("\nFailed to run migrations. Please check your database configuration.")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("\nFailed to create superuser account.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Ensure your MySQL server is running on 192.168.91.110:3306")
    print("2. Ensure your Redis server is running on 192.168.91.110:6379")
    print("3. Ensure your MinIO server is running on 192.168.91.110:9000")
    print("4. Start the development server:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python manage.py runserver")
    else:  # Unix/Linux/macOS
        print("   venv/bin/python manage.py runserver")
    
    print("5. Open your browser and go to http://127.0.0.1:8000/")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 