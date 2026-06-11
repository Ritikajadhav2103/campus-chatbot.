"""
View and analyze feedback data
"""
import os
import csv
from datetime import datetime

def view_feedback():
    """Display feedback statistics and recent entries"""
    
    feedback_file = "feedback.csv"
    
    if not os.path.exists(feedback_file):
        print("=" * 70)
        print("📊 FEEDBACK ANALYSIS")
        print("=" * 70)
        print("\n❌ No feedback file found yet.")
        print("\n💡 Feedback will be saved to 'feedback.csv' when users provide it.")
        print("\n🚀 Start the app and ask some questions to collect feedback:")
        print("   python -m streamlit run app_history.py")
        print("=" * 70)
        return
    
    # Read feedback
    with open(feedback_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        feedback_data = list(reader)
    
    if not feedback_data:
        print("=" * 70)
        print("📊 FEEDBACK ANALYSIS")
        print("=" * 70)
        print("\n📝 Feedback file exists but is empty.")
        print("\n💡 Users haven't provided feedback yet.")
        print("=" * 70)
        return
    
    # Calculate statistics
    total = len(feedback_data)
    helpful = sum(1 for f in feedback_data if f['Feedback'] == 'helpful')
    not_helpful = sum(1 for f in feedback_data if f['Feedback'] == 'not_helpful')
    satisfaction_rate = (helpful / total * 100) if total > 0 else 0
    
    print("=" * 70)
    print("📊 FEEDBACK ANALYSIS")
    print("=" * 70)
    
    print(f"\n📈 Overall Statistics:")
    print(f"  Total Feedback: {total}")
    print(f"  👍 Helpful: {helpful} ({helpful/total*100:.1f}%)")
    print(f"  👎 Not Helpful: {not_helpful} ({not_helpful/total*100:.1f}%)")
    print(f"  ⭐ Satisfaction Rate: {satisfaction_rate:.1f}%")
    
    # Recent feedback
    print(f"\n📝 Recent Feedback (Last 5):")
    print("-" * 70)
    
    for entry in feedback_data[-5:]:
        timestamp = datetime.fromisoformat(entry['Timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        feedback_icon = "👍" if entry['Feedback'] == 'helpful' else "👎"
        
        print(f"\n{feedback_icon} {entry['Feedback'].upper()} - {timestamp}")
        print(f"   Q: {entry['Question'][:60]}...")
        print(f"   A: {entry['Answer'][:60]}...")
    
    print("\n" + "=" * 70)
    print("💡 Tips:")
    print("  • Use this data to improve chatbot responses")
    print("  • Focus on questions with 'not helpful' feedback")
    print("  • Update handbook.txt with missing information")
    print("=" * 70)

if __name__ == "__main__":
    view_feedback()
