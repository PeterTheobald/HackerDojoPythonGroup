#!/usr/bin/env python3
"""
Test runner script for the transit tracking system
"""

import sys
import subprocess
import os

def run_tests():
    """Run all tests with proper configuration"""
    print("🧪 Running Transit Tracker Test Suite")
    print("=" * 50)
    
    # Configure Python environment
    configure_python_environment()
    
    # Run different test categories
    test_categories = [
        ("Unit Tests", ["test_location_tracker.py", "-m", "unit"]),
        ("Server Tests", ["test_server.py", "-m", "integration"]),
        ("Browser Tests", ["test_refresh_button.py", "-m", "browser"]),
        ("All Tests", ["test_*.py"])
    ]
    
    results = {}
    
    for category, args in test_categories:
        print(f"\n🔍 Running {category}...")
        print("-" * 30)
        
        try:
            # Run pytest with the specified arguments
            cmd = ["python", "-m", "pytest"] + args + ["-v"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            results[category] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            if result.returncode == 0:
                print(f"✅ {category} PASSED")
            else:
                print(f"❌ {category} FAILED")
                print("STDOUT:", result.stdout[-500:])  # Last 500 chars
                print("STDERR:", result.stderr[-500:])
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {category} TIMED OUT")
            results[category] = {'returncode': -1, 'error': 'timeout'}
            
        except Exception as e:
            print(f"💥 {category} ERROR: {e}")
            results[category] = {'returncode': -1, 'error': str(e)}
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r.get('returncode') == 0)
    total = len(results)
    
    for category, result in results.items():
        status = "✅ PASS" if result.get('returncode') == 0 else "❌ FAIL"
        print(f"{category:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check output above for details.")
        return 1

def configure_python_environment():
    """Ensure the Python environment is properly configured"""
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

def run_quick_tests():
    """Run only quick unit tests"""
    print("🚀 Running Quick Unit Tests")
    print("=" * 30)
    
    configure_python_environment()
    
    cmd = ["python", "-m", "pytest", "test_location_tracker.py", "-v", "--tb=short"]
    result = subprocess.run(cmd)
    return result.returncode

def run_browser_tests():
    """Run only browser tests"""
    print("🌐 Running Browser Tests")
    print("=" * 25)
    
    configure_python_environment()
    
    cmd = ["python", "-m", "pytest", "test_refresh_button.py", "-v", "-m", "browser"]
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            sys.exit(run_quick_tests())
        elif sys.argv[1] == "browser":
            sys.exit(run_browser_tests())
        else:
            print("Usage: python run_tests.py [quick|browser]")
            sys.exit(1)
    else:
        sys.exit(run_tests())
