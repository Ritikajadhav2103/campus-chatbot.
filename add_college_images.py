"""
Script to help add college images to the chatbot
"""

import json
import os
import shutil

# Load college database
with open('solapur_colleges_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create images folder if it doesn't exist
os.makedirs('data/college_images', exist_ok=True)

print("=" * 70)
print("COLLEGE IMAGE SETUP GUIDE")
print("=" * 70)
print()
print("This script will help you add images for each college.")
print()
print("INSTRUCTIONS:")
print("1. Save your college images in the 'data/college_images' folder")
print("2. Name them exactly as shown below")
print("3. Supported formats: .jpg, .jpeg, .png")
print()
print("=" * 70)
print()

# List all colleges and their expected image names
all_colleges = []
for category in data['categories'].values():
    all_colleges.extend(category['colleges'])

print(f"Total colleges: {len(all_colleges)}")
print()
print("EXPECTED IMAGE FILENAMES:")
print("-" * 70)

for idx, college in enumerate(all_colleges, 1):
    short_name = college['short_name'].lower().replace(' ', '_')
    image_name = f"{short_name}.jpg"
    image_path = f"data/college_images/{image_name}"
    
    # Check if image exists
    exists = "✅ EXISTS" if os.path.exists(image_path) else "❌ MISSING"
    
    print(f"{idx:2}. {college['name']}")
    print(f"    Filename: {image_name}")
    print(f"    Status: {exists}")
    print()

print("=" * 70)
print()
print("HOW TO ADD IMAGES:")
print()
print("1. Find/download college images")
print("2. Rename them to match the filenames above")
print("3. Copy them to: data/college_images/")
print("4. Run this script again to verify")
print()
print("EXAMPLE:")
print("  For 'Walchand Institute of Technology'")
print("  Save image as: data/college_images/wit.jpg")
print()
print("=" * 70)
print()

# Count existing images
existing_count = sum(1 for college in all_colleges 
                     if os.path.exists(f"data/college_images/{college['short_name'].lower().replace(' ', '_')}.jpg"))

print(f"Images added: {existing_count}/{len(all_colleges)}")
print()

if existing_count == 0:
    print("💡 TIP: Start by adding images for the most popular colleges:")
    print("   - WIT (Walchand Institute of Technology)")
    print("   - KBP (KBP College of Engineering)")
    print("   - DYP (D.Y. Patil Institute)")
    print("   - Government Medical College")
    print("   - Dayanand College")
print()
print("=" * 70)
