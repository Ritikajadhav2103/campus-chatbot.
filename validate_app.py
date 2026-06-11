"""
Validate app_history.py structure and initialization order
"""

def validate_initialization_order():
    """Check that session state is initialized before use"""
    
    with open("app_history.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Find line numbers
    init_line = None
    use_line = None
    
    for i, line in enumerate(lines):
        if 'if "dark_mode" not in st.session_state:' in line:
            init_line = i + 1
            print(f"✅ Session state initialization found at line {init_line}")
        
        if 'st.markdown(get_theme_css(st.session_state.dark_mode)' in line:
            use_line = i + 1
            print(f"✅ Theme CSS application found at line {use_line}")
    
    if init_line and use_line:
        if init_line < use_line:
            print(f"\n✅ CORRECT ORDER: Initialization (line {init_line}) comes before use (line {use_line})")
            print("✅ No AttributeError should occur!")
            return True
        else:
            print(f"\n❌ WRONG ORDER: Use (line {use_line}) comes before initialization (line {init_line})")
            print("❌ This will cause AttributeError!")
            return False
    else:
        print("\n⚠️ Could not find both initialization and use statements")
        return False

def check_duplicate_initialization():
    """Check for duplicate session state initialization"""
    
    with open("app_history.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    count = content.count('if "dark_mode" not in st.session_state:')
    
    if count == 1:
        print(f"\n✅ Single initialization found (no duplicates)")
        return True
    elif count > 1:
        print(f"\n⚠️ Found {count} initializations (duplicates exist)")
        return False
    else:
        print(f"\n❌ No initialization found!")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("VALIDATING APP_HISTORY.PY")
    print("=" * 60)
    
    order_ok = validate_initialization_order()
    no_duplicates = check_duplicate_initialization()
    
    print("\n" + "=" * 60)
    if order_ok and no_duplicates:
        print("✅ ALL CHECKS PASSED - App should run without errors!")
        print("\n🚀 Run the app with:")
        print("   python -m streamlit run app_history.py")
    else:
        print("❌ ISSUES FOUND - Please fix before running")
    print("=" * 60)
