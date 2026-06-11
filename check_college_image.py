"""
Check if college image is properly placed
"""
from pathlib import Path

image_path = Path("data/wit_college.jpg")

print("=" * 60)
print("CHECKING COLLEGE IMAGE")
print("=" * 60)

if image_path.exists():
    size = image_path.stat().st_size
    print(f"✅ Image found: {image_path}")
    print(f"✅ File size: {size:,} bytes ({size/1024:.1f} KB)")
    print("\n🎉 Your college photo is ready to display!")
else:
    print(f"❌ Image not found: {image_path}")
    print("\n📝 To add your college photo:")
    print("   1. Save your college photo as 'wit_college.jpg'")
    print("   2. Place it in the 'data' folder")
    print("   3. Full path should be: data/wit_college.jpg")
    print("\n💡 The app will use a placeholder until you add the image")

print("=" * 60)
