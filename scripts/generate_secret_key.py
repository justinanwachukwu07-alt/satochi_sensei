#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for the Satoshi Sensei application
"""

import secrets
import sys

def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    return secrets.token_urlsafe(32)

def main():
    """Main function to generate and display the secret key"""
    secret_key = generate_secret_key()
    
    print("Generated SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("Add this to your .env file:")
    print(f"SECRET_KEY={secret_key}")
    
    # Optionally write to a file
    if len(sys.argv) > 1 and sys.argv[1] == "--write":
        with open(".env", "a") as f:
            f.write(f"\nSECRET_KEY={secret_key}\n")
        print("\nSecret key has been written to .env file")

if __name__ == "__main__":
    main()
