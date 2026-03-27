"""
LLM-Powered Extraction Script with Relevance Scoring
Extracts entities, scores relevance, and prioritizes rabies survivor research papers
"""

import json
import streamlit as st
from groq import Groq
import time
import os
from datetime import datetime

def load_papers(filepath):
    """Load papers from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_and_score_paper(paper, client):
    """
    Use Llama 3.3 to extract entities AND score relevance for rabies survivors
    """
    
    title = paper.get('title', 'N/A')
    abstract = paper.get('abstract', 'N/A')
    
    prompt = f"""You are analyzing a rabies research paper to understand post-symptom rabies SURVIVAL factors.

TITLE: {title}

ABSTRACT: {abstract}

TASK: Extract key information AND score the relevance of this paper.

Please provide a structured analysis with these exact sections:

1. RELEVANCE_SCORE (1-10): How relevant is this paper to understanding rabies SURVIVORS?
   - 9-10: Directly about survivors or critical mechanisms
   - 7-8: Highly relevant to survival factors
   - 5-6: Moderately relevant (treatment, immunity, etc.)
   - 3-4: Tangentially related (general rabies)
   - 1-2: Not relevant to survivors

2. IS_SURVIVOR_FOCUSED (YES/NO): Does this paper directly discuss actual survivor cases or survival mechanisms?

3. SURVIVAL_FACTORS: What specific factors might contribute to survival? (genetic, immunological, treatment, viral strain, etc.)

4. IMMUNOLOGICAL_INSIGHTS: What immune mechanisms are discussed?

5. GENETIC_FACTORS: Any genetic/HLA predispositions mentioned?

6. TREATMENT_APPROACHES: What treatments are discussed?

7. CRITICAL_GAPS: What important information is only hinted at but needs full paper to understand?

8. KEY_FINDINGS: Single most important finding related to survivors

9. PRIORITY_LEVEL (HIGH/MEDIUM/LOW):
   - HIGH: Must read full paper (survivor cases, breakthrough findings, key mechanisms)
   - MEDIUM: Should read full paper (important supporting data)
   - LOW: Reference only (general background)

10. RECOMMEND_FULL_PAPER (YES/NO): Is the full paper worth getting?

Format your response EXACTLY like this JSON structure (use this exact format):
{{
  "relevance_score": [number 1-10],
  "is_survivor_focused": "[YES/NO]",
  "survival_factors": "[list of factors]",
  "immunological_insights": "[key immune mechanisms]",
  "genetic_factors": "[genetic info or 'Not mentioned']",
  "treatment_approaches": "[treatments discussed]",
  "critical_gaps": "[what's missing]",
  "key_findings": "[most important finding]",
  "priority_level": "[HIGH/MEDIUM/LOW]",
  "recommend_full_paper": "[YES/NO]"
}}

Be concise and factual. Extract only what is explicitly stated in the abstract."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=600,
            temperature=0.2  # Very low for consistent scoring
        )
        
        extracted_text = response.choices[0].message.content
        
        # Try to parse the JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = extracted_text.find('{')
            json_end = extracted_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = extracted_text[json_start:json_end]
                parsed_data = json.loads(json_str)
            else:
                parsed_data = {"raw_response": extracted_text}
        except:
            parsed_data = {"raw_response": extracted_text}
        
        return {
            "pubmed_id": paper.get('pubmed_id'),
            "title": title,
            "url": paper.get('url'),
            "journal": paper.get('journal'),
            "pub_date": paper.get('pub_date'),
            "extraction": parsed_data,
            "tokens_used": response.usage.total_tokens
        }
        
    except Exception as e:
        print(f"❌ Error extracting from {paper.get('pubmed_id')}: {e}")
        return None

def synthesize_top_papers(top_extractions, client):
    """
    Use Llama to synthesize findings from top-priority papers
    """
    
    # Build summary of top papers
    summary_text = ""
    for i, e in enumerate(top_extractions[:10], 1):
        extraction = e.get('extraction', {})
        summary_text += f"\n\nPaper {i}: {e['title']}\nPubMed ID: {e['pubmed_id']}\n"
        summary_text += f"Relevance Score: {extraction.get('relevance_score', 'N/A')}/10\n"
        summary_text += f"Survival Factors: {extraction.get('survival_factors', 'N/A')}\n"
        summary_text += f"Key Finding: {extraction.get('key_findings', 'N/A')}\n"
    
    synthesis_prompt = f"""You are synthesizing the TOP priority research papers on rabies survivors.

Here are the key papers and their findings:

{summary_text}

Based on these papers, provide a comprehensive synthesis addressing:

1. EMERGING PATTERNS: What common themes emerge about rabies survival?

2. GENETIC PREDISPOSITIONS: What genetic/HLA factors might enable survival?

3. IMMUNOLOGICAL MECHANISMS: How does the immune system enable survival in rare cases?

4. TREATMENT BREAKTHROUGHS: What treatment approaches show promise?

5. CRITICAL HYPOTHESES: Based on these papers, what testable hypotheses emerge for survival?

6. KNOWLEDGE GAPS: What critical questions remain unanswered that require the full papers?

7. NEXT STEPS: What specific information from full papers would be most valuable?

Provide evidence-based insights grounded in the papers analyzed."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Error in synthesis: {e}")
        return None

def save_extraction_results(results, filename):
    """Save extraction results to file"""
    os.makedirs("data/processed", exist_ok=True)
    filepath = os.path.join("data/processed", filename)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Saved results to: {filepath}")
    return filepath

def create_priority_report(all_extractions):
    """Create a prioritized report of papers"""
    
    # Sort by relevance score
    scored_papers = []
    for e in all_extractions:
        extraction = e.get('extraction', {})
        score = extraction.get('relevance_score', 0)
        priority = extraction.get('priority_level', 'LOW')
        
        scored_papers.append({
            'pubmed_id': e['pubmed_id'],
            'title': e['title'],
            'url': e['url'],
            'score': score if isinstance(score, (int, float)) else 0,
            'priority': priority,
            'is_survivor_focused': extraction.get('is_survivor_focused', 'NO'),
            'recommend_full_paper': extraction.get('recommend_full_paper', 'NO'),
            'key_findings': extraction.get('key_findings', 'N/A')
        })
    
    # Filter and sort
    high_priority = [p for p in scored_papers if p['priority'] == 'HIGH']
    medium_priority = [p for p in scored_papers if p['priority'] == 'MEDIUM']
    all_by_score = sorted(scored_papers, key=lambda x: x['score'], reverse=True)
    
    report = f"""
{'='*80}
RABIES SURVIVOR RESEARCH - PRIORITY PAPER REPORT
{'='*80}

SUMMARY:
- Total papers analyzed: {len(scored_papers)}
- HIGH priority papers: {len(high_priority)}
- MEDIUM priority papers: {len(medium_priority)}
- Average relevance score: {sum(p['score'] for p in scored_papers) / len(scored_papers):.1f}/10

{'='*80}
TOP 15 PAPERS BY RELEVANCE SCORE
{'='*80}

"""
    
    for i, paper in enumerate(all_by_score[:15], 1):
        report += f"\n{i}. [{paper['priority']} PRIORITY] {paper['title']}\n"
        report += f"   PubMed ID: {paper['pubmed_id']}\n"
        report += f"   Relevance Score: {paper['score']}/10\n"
        report += f"   Survivor Focused: {paper['is_survivor_focused']}\n"
        report += f"   Get Full Paper: {paper['recommend_full_paper']}\n"
        report += f"   URL: {paper['url']}\n"
        report += f"   Key Finding: {paper['key_findings'][:100]}...\n"
    
    report += f"\n\n{'='*80}\nHIGH PRIORITY PAPERS (MUST READ)\n{'='*80}\n\n"
    
    for i, paper in enumerate(high_priority, 1):
        report += f"{i}. {paper['title']}\n"
        report += f"   URL: {paper['url']}\n\n"
    
    return report

def main():
    """Main function"""
    
    # Load Groq API key
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except:
        print("❌ GROQ_API_KEY not found in secrets")
        return
    
    client = Groq(api_key=groq_api_key)
    
    print("=" * 80)
    print("RABV SURVIVOR RESEARCH - LLM EXTRACTION WITH RELEVANCE SCORING")
    print("=" * 80)
    print()
    
    # Load papers
    print("📂 Loading papers from data/raw/pubmed_abstracts_*.json...")
    import glob
    json_files = glob.glob("data/raw/pubmed_abstracts_*.json")
    
    if not json_files:
        print("❌ No papers found! Run data_collection.py first.")
        return
    
    latest_file = max(json_files, key=lambda f: os.path.getctime(f))
    papers = load_papers(latest_file)
    print(f"✅ Loaded {len(papers)} papers from {latest_file}\n")
    
    # Extract and score each paper
    print(f"🔄 Extracting, scoring, and analyzing {len(papers)} papers...\n")
    
    all_extractions = []
    tokens_used = 0
    high_priority_count = 0
    medium_priority_count = 0
    
    for idx, paper in enumerate(papers, 1):
        print(f"[{idx}/{len(papers)}] Processing {paper['pubmed_id'][:8]}... {paper['title'][:40]}...", end=" ")
        
        result = extract_and_score_paper(paper, client)
        
        if result:
            all_extractions.append(result)
            tokens_used += result['tokens_used']
            
            extraction = result.get('extraction', {})
            priority = extraction.get('priority_level', 'UNKNOWN')
            score = extraction.get('relevance_score', '?')
            
            if priority == 'HIGH':
                high_priority_count += 1
                print(f"✅ HIGH ({score}/10)")
            elif priority == 'MEDIUM':
                medium_priority_count += 1
                print(f"✅ MEDIUM ({score}/10)")
            else:
                print(f"✅ LOW ({score}/10)")
        else:
            print("❌ Failed")
        
        # Be nice to API
        time.sleep(0.4)
    
    print(f"\n{'='*80}")
    print(f"✅ Analyzed {len(all_extractions)} papers")
    print(f"📊 Total tokens used: {tokens_used}")
    print(f"🔴 HIGH priority: {high_priority_count}")
    print(f"🟡 MEDIUM priority: {medium_priority_count}")
    
    # Save extraction results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extractions_scored_{timestamp}.json"
    save_extraction_results(all_extractions, filename)
    
    # Create priority report
    print(f"\n{'='*80}")
    print("📋 Creating Priority Report...\n")
    report = create_priority_report(all_extractions)
    print(report)
    
    # Save report
    report_filename = f"priority_report_{timestamp}.txt"
    report_filepath = os.path.join("data/processed", report_filename)
    os.makedirs("data/processed", exist_ok=True)
    with open(report_filepath, 'w') as f:
        f.write(report)
    print(f"\n💾 Saved report to: {report_filepath}")
    
    # Synthesize top papers
    print(f"\n{'='*80}")
    print("🧠 Synthesizing insights from TOP priority papers...\n")
    
    top_papers = [e for e in all_extractions 
                  if e.get('extraction', {}).get('priority_level') == 'HIGH'][:10]
    
    if top_papers:
        synthesis = synthesize_top_papers(top_papers, client)
        
        if synthesis:
            print("📋 SYNTHESIS FROM TOP PAPERS:\n")
            print(synthesis)
            
            # Save synthesis
            synthesis_filename = f"synthesis_top_papers_{timestamp}.txt"
            synthesis_filepath = os.path.join("data/processed", synthesis_filename)
            with open(synthesis_filepath, 'w') as f:
                f.write(synthesis)
            print(f"\n💾 Saved synthesis to: {synthesis_filepath}")
    else:
        print("⚠️ No HIGH priority papers found for synthesis")
    
    print(f"\n{'='*80}")
    print("✅ LLM EXTRACTION & SCORING COMPLETE!")
    print(f"\nNext Steps:")
    print(f"1. Review the priority report: data/processed/priority_report_{timestamp}.txt")
    print(f"2. Get full PDFs for HIGH priority papers from:")
    print(f"   - PubMed Central: www.ncbi.nlm.nih.gov/pmc/")
    print(f"   - ResearchGate: www.researchgate.net/")
    print(f"   - Contact authors directly")
    print(f"3. Extract detailed information from full papers")
    print(f"4. Build final knowledge synthesis")

if __name__ == "__main__":
    main()