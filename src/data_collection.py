"""
Data Collection Script - XML PARSER VERSION
Fetches PubMed abstracts related to rabies survivors
"""

import requests
import json
import os
from datetime import datetime
import time
import xml.etree.ElementTree as ET

# PubMed API endpoints
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_abstracts(query, email, max_results=30):
    """
    Fetch abstracts from PubMed based on search query
    """
    
    print(f"🔍 Searching PubMed for: '{query}'")
    print(f"📊 Max results: {max_results}\n")
    
    # Step 1: Search for paper IDs (XML format)
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "tool": "rabv_analysis",
        "email": email
    }
    
    try:
        print(f"   Connecting to PubMed with email: {email}")
        search_response = requests.get(PUBMED_SEARCH_URL, params=search_params, timeout=10)
        
        if search_response.status_code != 200:
            print(f"   ❌ PubMed returned status {search_response.status_code}")
            return []
        
        # Parse XML response
        root = ET.fromstring(search_response.text)
        pubmed_ids = [id_elem.text for id_elem in root.findall('.//Id')]
        count = root.find('Count')
        total_count = int(count.text) if count is not None else 0
        
        print(f"   ✅ Found {total_count} papers | Fetching {len(pubmed_ids)} abstracts...\n")
        
        if not pubmed_ids:
            print("   ⚠️ No papers found for this query!")
            return []
        
        # Step 2: Fetch full records (XML format)
        papers = []
        for idx, pubmed_id in enumerate(pubmed_ids, 1):
            fetch_params = {
                "db": "pubmed",
                "id": pubmed_id,
                "rettype": "medline",
                "retmode": "xml",
                "tool": "rabv_analysis",
                "email": email
            }
            
            try:
                fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params, timeout=10)
                
                if fetch_response.status_code != 200:
                    print(f"   [{idx}/{len(pubmed_ids)}] ⚠️ Status {fetch_response.status_code}")
                    continue
                
                # Parse XML
                fetch_root = ET.fromstring(fetch_response.text)
                article_elem = fetch_root.find('.//Article')
                
                if article_elem is None:
                    continue
                
                # Extract title
                title_elem = article_elem.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else "N/A"
                
                # Extract abstract
                abstract_elem = article_elem.find('.//Abstract/AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else "N/A"
                
                # Extract journal
                journal_elem = article_elem.find('.//Journal/Title')
                journal = journal_elem.text if journal_elem is not None else "N/A"
                
                # Extract publication date
                pub_date_elem = article_elem.find('.//PubDate/Year')
                pub_date = pub_date_elem.text if pub_date_elem is not None else "N/A"
                
                # Extract authors
                authors = []
                for author_elem in article_elem.findall('.//Author'):
                    last_name = author_elem.find('LastName')
                    first_name = author_elem.find('ForeName')
                    if last_name is not None:
                        author_name = f"{last_name.text}"
                        if first_name is not None:
                            author_name = f"{first_name.text} {author_name}"
                        authors.append(author_name)
                
                paper_info = {
                    "pubmed_id": pubmed_id,
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "journal": journal,
                    "pub_date": pub_date,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
                }
                
                papers.append(paper_info)
                print(f"   [{idx}/{len(pubmed_ids)}] ✅ {title[:50]}...")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"   [{idx}/{len(pubmed_ids)}] ❌ Error: {str(e)[:50]}")
                continue
        
        return papers
    
    except Exception as e:
        print(f"   ❌ Search error: {e}")
        return []


def save_to_json(data, filename):
    """Save data to JSON file"""
    os.makedirs("data/raw", exist_ok=True)
    filepath = os.path.join("data/raw", filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Saved {len(data)} papers to: {filepath}")
    return filepath


def main():
    """Main function"""
    
    # Get email from environment or use actual email
    try:
        import streamlit as st
        email = st.secrets.get("PUBMED_EMAIL", "khalid.preneurlab07@gmail.com")
    except:
        email = os.getenv("PUBMED_EMAIL", "khalid.preneurlab07@gmail.com")
    
    print("=" * 70)
    print("RABV SURVIVOR RESEARCH - DATA COLLECTION")
    print("=" * 70)
    print()
    
    # Search queries for rabies survivor research
    search_queries = [
        "rabies survivors post-symptom",
        "rabies Milwaukee Protocol",
        "human rabies survival",
        "rabies survivor immunology",
        "Jeanna Giese rabies",
    ]
    
    all_papers = []
    
    for i, query in enumerate(search_queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/{len(search_queries)}")
        print(f"{'='*70}\n")
        
        papers = fetch_pubmed_abstracts(query, email, max_results=30)
        all_papers.extend(papers)
        
        if i < len(search_queries):
            print("   Waiting before next query...")
            time.sleep(2)
    
    # Remove duplicates (by pubmed_id)
    unique_papers = {p['pubmed_id']: p for p in all_papers}
    unique_papers = list(unique_papers.values())
    
    print(f"\n{'='*70}")
    print(f"📊 Total unique papers collected: {len(unique_papers)}")
    
    # Save to file
    if unique_papers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pubmed_abstracts_{timestamp}.json"
        save_to_json(unique_papers, filename)
        
        # Print sample
        print(f"\n📄 Sample paper:")
        sample = unique_papers[0]
        print(f"   Title: {sample['title'][:70]}")
        print(f"   PubMed ID: {sample['pubmed_id']}")
        print(f"   URL: {sample['url']}")
        print(f"\n✅ Data collection complete!")
    else:
        print("\n⚠️ No papers collected!")


if __name__ == "__main__":
    main()