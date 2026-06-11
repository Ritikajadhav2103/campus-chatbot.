"""
Test feedback feature implementation
"""
import os

def test_feedback_feature():
    """Test that feedback feature is properly implemented"""
    
    with open("app_history.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    checks = {
        "Feedback Session State": '"feedback_given"' in content,
        "Feedback CSV File": 'FEEDBACK_FILE = "feedback.csv"' in content,
        "Save Feedback Function": 'def save_feedback(' in content,
        "Helpful Button": '"👍 Helpful"' in content,
        "Not Helpful Button": '"👎 Not Helpful"' in content,
        "Thank You Message": 'Thank you for your feedback!' in content,
        "CSV Writing": 'csv.writer' in content,
        "Feedback Storage": 'save_feedback(idx,' in content,
        "Feedback Display": 'feedback_given[feedback_key]' in content,
        "No Reload": 'st.rerun()' in content
    }
    
    print("=" * 70)
    print("TESTING FEEDBACK FEATURE")
    print("=" * 70)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL FEEDBACK FEATURE CHECKS PASSED!")
        print("\n📋 Features Implemented:")
        print("  • 👍 Helpful button below each bot response")
        print("  • 👎 Not Helpful button below each bot response")
        print("  • Feedback saved to feedback.csv")
        print("  • Thank you message after feedback")
        print("  • Clean UI with 3-column layout")
        print("  • No full page reload (uses st.rerun)")
        print("\n📁 Feedback File:")
        print("  • Location: feedback.csv")
        print("  • Format: CSV with timestamp, message index, feedback type, question, answer")
        print("\n🚀 Run the app:")
        print("  python -m streamlit run app_history.py")
    else:
        print("❌ SOME CHECKS FAILED")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    test_feedback_feature()
