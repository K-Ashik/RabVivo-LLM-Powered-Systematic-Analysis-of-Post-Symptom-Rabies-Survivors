import requests

email = "khalid.preneurlab07@gmail.com"
query = "rabies survivors"

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

search_params = {
    "db": "pubmed",
    "term": query,
    "retmax": 5,
    "rettype": "json",
    "tool": "rabv_analysis",
    "email": email
}

print(f"🔍 Attempting to connect to PubMed...")
print(f"   URL: {PUBMED_SEARCH_URL}")
print(f"   Query: {query}")
print(f"   Email: {email}\n")

try:
    response = requests.get(PUBMED_SEARCH_URL, params=search_params, timeout=10)
    
    print(f"✅ Response received!")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Response Length: {len(response.text)} characters")
    print(f"\n📄 Response Text (first 500 chars):")
    print(f"   {response.text[:500]}\n")
    
    # Try parsing as JSON
    try:
        data = response.json()
        print(f"✅ Successfully parsed as JSON")
        print(f"   Keys: {list(data.keys())}")
    except Exception as e:
        print(f"❌ Failed to parse as JSON: {e}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")