#!/usr/bin/env python3
"""
Quick test to verify Supabase connection works
"""

try:
    from supabase import create_client, Client
    print("✅ supabase-py library installed")
except ImportError:
    print("❌ supabase-py not installed. Run: pip install supabase")
    exit(1)

# Test connection
SUPABASE_URL = "https://iteavenjozhzxupbxosu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0ZWF2ZW5qb3poenh1cGJ4b3N1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwMjk4NTgsImV4cCI6MjA3ODYwNTg1OH0.AfBGdanvvHUoFOWYF94PN0ccLlWPVJFHN1At-kjzpkE"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client created successfully")

    # Try to list tables
    result = supabase.table('interview_questions').select("*").limit(1).execute()
    print(f"✅ Connected to Supabase! Found {len(result.data)} row(s) in interview_questions table")

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nThis might mean:")
    print("1. The 'interview_questions' table doesn't exist yet (we'll create it)")
    print("2. Network issue")
    print("3. Invalid credentials")
