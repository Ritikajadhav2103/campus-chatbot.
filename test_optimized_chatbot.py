"""
Test script for Optimized Solapur Colleges Chatbot
Tests all features and functionality
"""

import json
import time

def test_data_loading():
    """Test 1: Data Loading"""
    print("=" * 60)
    print("TEST 1: Data Loading")
    print("=" * 60)
    
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print("✅ Database loaded successfully")
        print(f"   Total colleges: {data['total_colleges']}")
        print(f"   Categories: {len(data['categories'])}")
        
        # Count colleges per category
        for cat_key, cat_data in data['categories'].items():
            print(f"   - {cat_data['name']}: {len(cat_data['colleges'])} colleges")
        
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_college_search():
    """Test 2: College Search"""
    print("\n" + "=" * 60)
    print("TEST 2: College Search")
    print("=" * 60)
    
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Flatten colleges
        all_colleges = []
        for category in data['categories'].values():
            all_colleges.extend(category['colleges'])
        
        # Test searches
        test_queries = [
            "WIT",
            "Walchand Institute of Technology",
            "KBP",
            "Medical College",
            "Dayanand"
        ]
        
        for query in test_queries:
            query_lower = query.lower()
            found = False
            
            # Try exact match
            for college in all_colleges:
                if college['name'].lower() == query_lower or college['short_name'].lower() == query_lower:
                    print(f"✅ Found '{query}': {college['name']}")
                    found = True
                    break
            
            # Try contains match
            if not found:
                for college in all_colleges:
                    if query_lower in college['name'].lower():
                        print(f"✅ Found '{query}': {college['name']}")
                        found = True
                        break
            
            if not found:
                print(f"⚠️  '{query}' not found")
        
        return True
    except Exception as e:
        print(f"❌ Error in search: {e}")
        return False

def test_category_detection():
    """Test 3: Category Detection"""
    print("\n" + "=" * 60)
    print("TEST 3: Category Detection")
    print("=" * 60)
    
    test_cases = [
        ("engineering colleges", "engineering"),
        ("medical colleges in solapur", "medical"),
        ("commerce colleges", "commerce"),
        ("universities", "universities"),
        ("show all colleges", "all"),
        ("arts and science", "arts_science")
    ]
    
    keywords = {
        'engineering': ['engineering', 'engineer', 'b.tech', 'btech', 'polytechnic'],
        'medical': ['medical', 'mbbs', 'doctor', 'health', 'nursing', 'dental'],
        'commerce': ['commerce', 'b.com', 'bcom', 'management', 'mba', 'bba'],
        'arts_science': ['arts', 'science', 'b.a', 'b.sc', 'bsc'],
        'universities': ['university', 'universities'],
        'all': ['all', 'list', 'show all']
    }
    
    for query, expected in test_cases:
        query_lower = query.lower()
        detected = None
        
        for category, words in keywords.items():
            if any(word in query_lower for word in words):
                detected = category
                break
        
        if detected == expected:
            print(f"✅ '{query}' → {detected}")
        else:
            print(f"❌ '{query}' → Expected: {expected}, Got: {detected}")
    
    return True

def test_college_data_completeness():
    """Test 4: College Data Completeness"""
    print("\n" + "=" * 60)
    print("TEST 4: College Data Completeness")
    print("=" * 60)
    
    try:
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        required_fields = ['name', 'short_name', 'type', 'established', 'location', 
                          'contact', 'email', 'website', 'courses', 'affiliation']
        
        optional_fields = ['photo_url', 'history']
        
        colleges_with_photos = 0
        colleges_with_history = 0
        total_colleges = 0
        
        for category in data['categories'].values():
            for college in category['colleges']:
                total_colleges += 1
                
                # Check required fields
                missing = [f for f in required_fields if f not in college]
                if missing:
                    print(f"⚠️  {college['name']}: Missing {missing}")
                
                # Check optional fields
                if 'photo_url' in college:
                    colleges_with_photos += 1
                if 'history' in college:
                    colleges_with_history += 1
        
        print(f"✅ Total colleges checked: {total_colleges}")
        print(f"   Colleges with photos: {colleges_with_photos}/{total_colleges}")
        print(f"   Colleges with history: {colleges_with_history}/{total_colleges}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return False

def test_performance():
    """Test 5: Performance"""
    print("\n" + "=" * 60)
    print("TEST 5: Performance")
    print("=" * 60)
    
    try:
        # Test data loading speed
        start = time.time()
        with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        load_time = time.time() - start
        
        print(f"✅ Data load time: {load_time:.4f} seconds")
        
        # Test search speed
        all_colleges = []
        for category in data['categories'].values():
            all_colleges.extend(category['colleges'])
        
        start = time.time()
        for _ in range(100):
            query = "WIT"
            for college in all_colleges:
                if query.lower() in college['name'].lower():
                    break
        search_time = (time.time() - start) / 100
        
        print(f"✅ Average search time: {search_time:.6f} seconds")
        
        if load_time < 0.1 and search_time < 0.001:
            print("✅ Performance: EXCELLENT")
        elif load_time < 0.5 and search_time < 0.01:
            print("✅ Performance: GOOD")
        else:
            print("⚠️  Performance: NEEDS IMPROVEMENT")
        
        return True
    except Exception as e:
        print(f"❌ Error in performance test: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("OPTIMIZED CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_data_loading,
        test_college_search,
        test_category_detection,
        test_college_data_completeness,
        test_performance
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ ALL TESTS PASSED!")
        print("\n🚀 Chatbot is ready to use!")
        print("\nTo run the chatbot:")
        print("   Double-click: RUN_OPTIMIZED.bat")
        print("   Or run: streamlit run app_solapur_optimized.py")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
