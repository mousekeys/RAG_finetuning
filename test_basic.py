"""
Simple test script for the RAG Finance Tracking API
Tests basic functionality without requiring the embedding model to be downloaded
"""

import sys
import importlib.util

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'fastapi',
        'uvicorn',
        'chromadb',
        'pydantic',
    ]
    
    for module in required_modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                print(f"✗ {module} - NOT FOUND")
                return False
            print(f"✓ {module} - OK")
        except Exception as e:
            print(f"✗ {module} - ERROR: {e}")
            return False
    
    return True

def test_main_structure():
    """Test that main.py has the expected structure"""
    print("\nTesting main.py structure...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check for key components
        checks = [
            ('FastAPI app creation', 'app = FastAPI'),
            ('CORS middleware', 'CORSMiddleware'),
            ('ChromaDB client', 'chromadb.PersistentClient'),
            ('Root endpoint', '@app.get("/")'),
            ('Health endpoint', '@app.get("/health")'),
            ('Add document endpoint', '@app.post("/documents/add")'),
            ('Query endpoint', '/query'),
            ('Document count endpoint', '@app.get("/documents/count")'),
            ('Clear documents endpoint', '@app.delete("/documents/clear")'),
        ]
        
        all_passed = True
        for name, check in checks:
            if check in content:
                print(f"✓ {name} - OK")
            else:
                print(f"✗ {name} - MISSING")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error reading main.py: {e}")
        return False

def test_android_structure():
    """Test that Android app structure is correct"""
    print("\nTesting Android app structure...")
    
    import os
    
    required_files = [
        'android_app/build.gradle',
        'android_app/settings.gradle',
        'android_app/src/main/AndroidManifest.xml',
        'android_app/src/main/java/com/financetracking/rag/MainActivity.kt',
        'android_app/src/main/java/com/financetracking/rag/network/FinanceApiService.kt',
        'android_app/src/main/java/com/financetracking/rag/network/ApiClient.kt',
        'android_app/src/main/java/com/financetracking/rag/data/FinanceRepository.kt',
        'android_app/src/main/java/com/financetracking/rag/viewmodel/FinanceViewModel.kt',
        'android_app/src/main/java/com/financetracking/rag/ui/FinanceScreen.kt',
        'android_app/src/main/res/values/strings.xml',
    ]
    
    all_exist = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath} - OK")
        else:
            print(f"✗ {filepath} - MISSING")
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test that documentation files exist and are not empty"""
    print("\nTesting documentation...")
    
    import os
    
    doc_files = ['README.md', 'EXAMPLES.md', 'requirements.txt']
    
    all_good = True
    for filepath in doc_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            if size > 100:  # Should have substantial content
                print(f"✓ {filepath} - OK ({size} bytes)")
            else:
                print(f"✗ {filepath} - Too small ({size} bytes)")
                all_good = False
        else:
            print(f"✗ {filepath} - MISSING")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("=" * 60)
    print("RAG Finance Tracking - Basic Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Import Test", test_imports()))
    results.append(("Main.py Structure Test", test_main_structure()))
    results.append(("Android Structure Test", test_android_structure()))
    results.append(("Documentation Test", test_documentation()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
