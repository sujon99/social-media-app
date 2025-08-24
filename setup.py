#!/usr/bin/env python3
"""
Setup script for Social Media Application
This script helps set up the application with proper configuration.
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def setup_database():
    """Set up database configuration"""
    print("🔍 Setting up database...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    # Get database configuration from user
    print("\n📊 Database Configuration:")
    db_host = input("Enter database host (default: localhost): ").strip() or "localhost"
    db_port = input("Enter database port (default: 3306): ").strip() or "3306"
    db_name = input("Enter database name (default: mydb): ").strip() or "mydb"
    db_user = input("Enter database user (default: myuser): ").strip() or "myuser"
    db_password = getpass.getpass("Enter database password (default: mypassword): ").strip() or "mypassword"
    
    # Get Redis configuration
    print("\n🔴 Redis Configuration:")
    redis_host = input("Enter Redis host (default: localhost): ").strip() or "localhost"
    redis_port = input("Enter Redis port (default: 6379): ").strip() or "6379"
    
    # Get MinIO configuration
    print("\n📦 MinIO Configuration:")
    minio_host = input("Enter MinIO host (default: localhost): ").strip() or "localhost"
    minio_port = input("Enter MinIO port (default: 9000): ").strip() or "9000"
    minio_access_key = input("Enter MinIO access key (default: minioadmin): ").strip() or "minioadmin"
    minio_secret_key = getpass.getpass("Enter MinIO secret key (default: minioadmin123): ").strip() or "minioadmin123"
    
    # Get server configuration
    print("\n🌐 Server Configuration:")
    server_host = input("Enter server host/IP (default: localhost): ").strip() or "localhost"
    
    # Create .env file
    env_content = f"""# =============================================================================
# Social Media App Environment Configuration
# =============================================================================

# =============================================================================
# Database Configuration (MySQL)
# =============================================================================
DATABASE_HOST={db_host}
DATABASE_PORT={db_port}
DATABASE_NAME={db_name}
DATABASE_USER={db_user}
DATABASE_PASSWORD={db_password}

# =============================================================================
# Redis Configuration (Session Storage)
# =============================================================================
REDIS_HOST={redis_host}
REDIS_PORT={redis_port}

# =============================================================================
# MinIO Configuration (Object Storage)
# =============================================================================
MINIO_HOST={minio_host}
MINIO_PORT={minio_port}
MINIO_ACCESS_KEY={minio_access_key}
MINIO_SECRET_KEY={minio_secret_key}
MINIO_BUCKET_NAME=social-media-app
MINIO_USE_HTTPS=false

# =============================================================================
# Server Configuration
# =============================================================================
SERVER_HOST={server_host}

# =============================================================================
# Django Configuration (Optional - Advanced)
# =============================================================================
# SECRET_KEY=your-secret-key-here
# DEBUG=false
# ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def run_migrations():
    """Run Django migrations"""
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    return True

def collect_static():
    """Collect static files"""
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    return True

def create_superuser():
    """Create a superuser account"""
    print("👤 Creating superuser account...")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Superuser creation skipped or failed")
        return True  # Don't fail the setup if superuser creation fails

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    if not run_command("python test_app.py", "Running test suite"):
        print("⚠️  Tests failed, but setup will continue")
        return True
    return True

def main():
    """Main setup function"""
    print("🚀 Social Media Application Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Setup database configuration
    if not setup_database():
        return 1
    
    # Run migrations
    if not run_migrations():
        return 1
    
    # Collect static files
    if not collect_static():
        return 1
    
    # Create superuser
    create_superuser()
    
    # Run tests
    run_tests()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Ensure your external services are running:")
    print(f"   - MySQL server on {os.getenv('DATABASE_HOST', 'localhost')}:{os.getenv('DATABASE_PORT', '3306')}")
    print(f"   - Redis server on {os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', '6379')}")
    print(f"   - MinIO server on {os.getenv('MINIO_HOST', 'localhost')}:{os.getenv('MINIO_PORT', '9000')}")
    print("2. Start the development server: python manage.py runserver")
    print("3. Open your browser and go to http://127.0.0.1:8000/")
    print("4. Create a new account and start using the application!")
    print("\n🚀 Your social media application is ready!")
    
    return 0

if __name__ == "__main__":
    exit(main()) 