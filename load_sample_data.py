"""
Sample data loader for RAG Finance Tracking
This script populates the database with sample financial documents for testing.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Sample financial documents
SAMPLE_DOCUMENTS = [
    # Income
    {
        "text": "Monthly salary payment from ABC Corporation",
        "category": "Income",
        "amount": 5500.00,
        "date": "2024-01-01"
    },
    {
        "text": "Freelance web development project for XYZ Company",
        "category": "Income",
        "amount": 2500.00,
        "date": "2024-01-15"
    },
    {
        "text": "Dividend payment from stock portfolio",
        "category": "Income",
        "amount": 350.00,
        "date": "2024-01-20"
    },
    {
        "text": "Cash bonus for project completion",
        "category": "Income",
        "amount": 1000.00,
        "date": "2024-01-25"
    },
    
    # Expenses - Housing
    {
        "text": "Monthly rent payment for apartment",
        "category": "Expense",
        "amount": 1500.00,
        "date": "2024-01-01"
    },
    {
        "text": "Electric utility bill for January",
        "category": "Expense",
        "amount": 89.99,
        "date": "2024-01-10"
    },
    {
        "text": "Internet and cable service monthly fee",
        "category": "Expense",
        "amount": 95.00,
        "date": "2024-01-05"
    },
    
    # Expenses - Food
    {
        "text": "Grocery shopping at Whole Foods Market",
        "category": "Expense",
        "amount": 156.75,
        "date": "2024-01-03"
    },
    {
        "text": "Weekly groceries at Trader Joe's",
        "category": "Expense",
        "amount": 87.50,
        "date": "2024-01-10"
    },
    {
        "text": "Restaurant dinner with family at Italian place",
        "category": "Expense",
        "amount": 125.00,
        "date": "2024-01-14"
    },
    {
        "text": "Coffee and breakfast at local cafe",
        "category": "Expense",
        "amount": 18.50,
        "date": "2024-01-16"
    },
    
    # Expenses - Transportation
    {
        "text": "Gas station fill-up for car",
        "category": "Expense",
        "amount": 55.00,
        "date": "2024-01-07"
    },
    {
        "text": "Car insurance premium payment",
        "category": "Expense",
        "amount": 180.00,
        "date": "2024-01-02"
    },
    {
        "text": "Uber ride to airport",
        "category": "Expense",
        "amount": 42.00,
        "date": "2024-01-18"
    },
    
    # Expenses - Entertainment
    {
        "text": "Movie tickets and snacks at cinema",
        "category": "Expense",
        "amount": 45.00,
        "date": "2024-01-12"
    },
    {
        "text": "Netflix monthly subscription",
        "category": "Expense",
        "amount": 15.99,
        "date": "2024-01-01"
    },
    {
        "text": "Spotify premium subscription",
        "category": "Expense",
        "amount": 9.99,
        "date": "2024-01-01"
    },
    
    # Investments
    {
        "text": "Purchased 5 shares of Apple stock (AAPL)",
        "category": "Investment",
        "amount": 875.00,
        "date": "2024-01-08"
    },
    {
        "text": "Monthly 401k retirement contribution",
        "category": "Investment",
        "amount": 550.00,
        "date": "2024-01-01"
    },
    {
        "text": "Investment in cryptocurrency - Bitcoin",
        "category": "Investment",
        "amount": 500.00,
        "date": "2024-01-22"
    },
    
    # Savings
    {
        "text": "Transfer to emergency savings account",
        "category": "Savings",
        "amount": 800.00,
        "date": "2024-01-01"
    },
    {
        "text": "Deposit to high-yield savings account",
        "category": "Savings",
        "amount": 500.00,
        "date": "2024-01-15"
    },
    
    # Healthcare
    {
        "text": "Doctor visit copay",
        "category": "Expense",
        "amount": 35.00,
        "date": "2024-01-11"
    },
    {
        "text": "Prescription medication at pharmacy",
        "category": "Expense",
        "amount": 25.00,
        "date": "2024-01-12"
    },
    
    # Shopping
    {
        "text": "New laptop for work from Best Buy",
        "category": "Expense",
        "amount": 1299.99,
        "date": "2024-01-20"
    },
    {
        "text": "Clothing shopping at department store",
        "category": "Expense",
        "amount": 185.00,
        "date": "2024-01-17"
    },
]


def check_health():
    """Check if the backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Backend is healthy")
            return True
        else:
            print(f"✗ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to backend: {e}")
        print(f"  Make sure the backend is running at {BASE_URL}")
        return False


def clear_existing_data():
    """Clear existing documents"""
    try:
        response = requests.delete(f"{BASE_URL}/documents/clear")
        if response.status_code == 200:
            print("✓ Cleared existing documents")
            return True
        else:
            print(f"✗ Failed to clear documents: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error clearing documents: {e}")
        return False


def load_sample_data():
    """Load sample documents into the database"""
    print(f"\nLoading {len(SAMPLE_DOCUMENTS)} sample documents...")
    
    success_count = 0
    error_count = 0
    
    for i, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/documents/add",
                json=doc,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f"  [{i}/{len(SAMPLE_DOCUMENTS)}] ✓ Added: {doc['text'][:50]}...")
            else:
                error_count += 1
                print(f"  [{i}/{len(SAMPLE_DOCUMENTS)}] ✗ Failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"  [{i}/{len(SAMPLE_DOCUMENTS)}] ✗ Error: {e}")
    
    return success_count, error_count


def get_document_count():
    """Get the total count of documents"""
    try:
        response = requests.get(f"{BASE_URL}/documents/count")
        if response.status_code == 200:
            count = response.json()["count"]
            print(f"\n✓ Total documents in database: {count}")
            return count
        else:
            print(f"✗ Failed to get count: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Error getting count: {e}")
        return None


def main():
    """Main function"""
    print("=" * 60)
    print("RAG Finance Tracking - Sample Data Loader")
    print("=" * 60)
    
    # Check backend health
    if not check_health():
        print("\nPlease start the backend server first:")
        print("  python main.py")
        return 1
    
    # Ask user if they want to clear existing data
    print("\nDo you want to clear existing data before loading? (y/N): ", end="")
    try:
        choice = input().strip().lower()
        if choice == 'y':
            if not clear_existing_data():
                print("Failed to clear data. Continue anyway? (y/N): ", end="")
                if input().strip().lower() != 'y':
                    return 1
    except KeyboardInterrupt:
        print("\nCancelled by user")
        return 1
    
    # Load sample data
    success, errors = load_sample_data()
    
    # Display summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Successfully loaded: {success}")
    print(f"Errors: {errors}")
    
    # Get final count
    get_document_count()
    
    # Sample queries
    print("\n" + "=" * 60)
    print("Try these sample queries:")
    print("=" * 60)
    print("1. What are my total expenses?")
    print("2. Show me all my income sources")
    print("3. What did I invest in?")
    print("4. How much did I spend on food?")
    print("5. What are my monthly subscriptions?")
    
    print("\nYou can test these using:")
    print("- The Android app (Query tab)")
    print(f"- The API: curl -X POST '{BASE_URL}/query' -H 'Content-Type: application/json' -d '{{\"query\": \"YOUR_QUESTION\"}}'")
    print(f"- The web docs: {BASE_URL}/docs")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
