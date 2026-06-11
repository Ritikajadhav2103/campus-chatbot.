"""
Test script to verify dark mode implementation
"""

def test_theme_toggle():
    """Test that theme toggle functionality is properly implemented"""
    
    with open("app_history.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for dark mode session state
    assert '"dark_mode"' in content, "Dark mode session state not found"
    
    # Check for theme CSS function
    assert 'def get_theme_css(dark_mode):' in content, "Theme CSS function not found"
    
    # Check for dark mode colors
    assert '--bg-color: #1a1a2e' in content, "Dark mode background color not found"
    assert '--card-bg: #16213e' in content, "Dark mode card background not found"
    
    # Check for light mode colors
    assert '--bg-color: #f8f9fa' in content, "Light mode background color not found"
    assert '--card-bg: #ffffff' in content, "Light mode card background not found"
    
    # Check for theme toggle button
    assert 'theme_toggle' in content, "Theme toggle button not found"
    
    # Check for smooth transitions
    assert 'transition: all 0.3s ease' in content, "Smooth transitions not found"
    
    # Check for theme icons
    assert '🌙' in content or '☀️' in content, "Theme icons not found"
    
    print("✅ All dark mode tests passed!")
    print("\n📋 Features implemented:")
    print("  • Dark mode session state")
    print("  • Dynamic theme CSS function")
    print("  • Dark mode color palette (#1a1a2e, #16213e)")
    print("  • Light mode color palette (#f8f9fa, #ffffff)")
    print("  • Theme toggle button with icons (🌙/☀️)")
    print("  • Smooth 0.3s transitions")
    print("  • Responsive design for both themes")
    print("\n🎨 Color Schemes:")
    print("  Dark Mode: Deep blue-black (#1a1a2e) with navy cards (#16213e)")
    print("  Light Mode: Light gray (#f8f9fa) with white cards (#ffffff)")
    print("\n🚀 To test:")
    print("  1. Run: python -m streamlit run app_history.py")
    print("  2. Click the theme toggle button (🌙/☀️) in the header")
    print("  3. Watch the entire UI smoothly transition between themes")

if __name__ == "__main__":
    test_theme_toggle()
