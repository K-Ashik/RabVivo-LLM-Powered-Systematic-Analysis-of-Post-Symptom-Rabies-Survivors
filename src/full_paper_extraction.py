"""
Full Paper Extraction Script
Extracts detailed data from PDF papers using Groq LLM
Handles multi-language papers (including Russian)
"""

import os
import json
import streamlit as st
from groq import Groq
import time
from datetime import datetime

try:
    import PyPDF2
except ImportError:
    print("⚠️ PyPDF2 not installed. Install with: pip install PyPDF2")

def detect_russian_content(text):
    """
    Detect if text contains Russian language by checking for Cyrillic characters
    Russian Cyrillic characters: U+0400 to U+04FF
    """
    russian_chars = 0
    sample_text = text[:2000]  # Check first 2000 characters
    
    for char in sample_text:
        # Cyrillic Unicode range
        if '\u0400' <= char <= '\u04ff':
            russian_chars += 1
    
    # If more than 5% of characters are Cyrillic, mark as Russian
    percentage = (russian_chars / max(1, len(sample_text))) * 100
    is_russian = percentage > 5
    
    if is_russian:
        print(f"   🇷🇺 Russian content detected ({percentage:.1f}% Cyrillic)")
    
    return is_russian

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            # Extract first 5 pages (usually contains key info)
            for page_num in range(min(5, num_pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        return text, num_pages
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None, None

def analyze_full_paper(pdf_text, paper_title, client, is_russian=False):
    """
    Use Llama to extract detailed information from full paper
    Handles both English and Russian papers
    """
    
    # Truncate text if too long (keep most relevant parts)
    if len(pdf_text) > 8000:
        pdf_text = pdf_text[:8000] + "\n... [text truncated] ..."
    
    language_note = " [NOTE: This paper is in Russian - extracting key information]" if is_russian else ""
    
    prompt = f"""You are analyzing a FULL RESEARCH PAPER on rabies survivors.{language_note}

PAPER TITLE: {paper_title}

EXTRACTED TEXT (first pages):
{pdf_text}

Please extract and structure the following detailed information:

1. PATIENT CASES:
   - Number of patient cases discussed
   - Patient demographics (age, gender, exposure type)
   - Country/region
   - Survival status (survived/died)
   - Time from symptom onset to outcome

2. GENETIC FACTORS:
   - Any HLA typing mentioned?
   - Genetic predispositions?
   - Family history?
   - Specific genetic markers?

3. IMMUNOLOGICAL MARKERS:
   - Antibody responses (neutralizing antibodies, titers)
   - T-cell responses (CD8+, CD4+ counts)
   - Cytokine profiles (IL-6, TNF-alpha, IFN-gamma, etc.)
   - Vaccine response?
   - Prior vaccination status?

4. TREATMENT PROTOCOLS:
   - Specific drugs used (antivirals, sedatives, etc.)
   - Dosages and durations
   - Milwaukee Protocol used?
   - Medically induced coma?
   - ICU support details

5. CLINICAL PRESENTATION:
   - Symptom progression
   - Time from exposure to symptom onset
   - Type of rabies (furious vs. paralytic)
   - Neurological symptoms detailed

6. OUTCOMES:
   - Survival duration
   - Recovery status
   - Neurological sequelae (long-term effects)
   - Quality of life post-recovery
   - Full recovery vs. permanent disability

7. KEY MECHANISMS ENABLING SURVIVAL:
   - What factors appear to enable survival?
   - Immune response characteristics?
   - Viral load dynamics?
   - Timing of interventions?

8. CRITICAL DATA (specific numbers/values):
   - Patient ages
   - Survival rates
   - Antibody titers
   - Recovery timeframes
   - Any quantitative data

9. NOVEL FINDINGS:
   - What new insights does this paper provide?
   - Unusual cases?
   - Breakthrough findings?

10. LIMITATIONS & GAPS:
    - What data is incomplete?
    - What would strengthen the findings?

Format your response as a structured analysis. Be thorough and extract ALL quantitative data (numbers, percentages, timeframes). If information is not available in the excerpt, state "Not provided in excerpt"."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Error analyzing paper: {e}")
        return None

def save_results(results, filename):
    """Save extraction results"""
    os.makedirs("data/processed", exist_ok=True)
    filepath = os.path.join("data/processed", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {filepath}")
    return filepath

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
    print("FULL PAPER EXTRACTION - DETAILED DATA MINING")
    print("=" * 80)
    print()
    
    # Find PDF files
    pdf_folder = "data/raw/full_papers"
    
    if not os.path.exists(pdf_folder):
        print(f"❌ Folder not found: {pdf_folder}")
        print("Please create data/raw/full_papers/ and add your PDF files")
        return
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_folder}")
        return
    
    print(f"📂 Found {len(pdf_files)} PDF files\n")
    
    all_extractions = []
    
    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
        print(f"{'='*80}\n")
        
        # Extract text first
        print("📄 Extracting text from PDF...", end=" ")
        pdf_text, num_pages = extract_text_from_pdf(pdf_path)
        
        if pdf_text is None:
            print("❌ Failed to read PDF")
            continue
        
        print(f"✅ ({num_pages} pages)")
        
        # Check if Russian (both filename AND content detection)
        print("   Detecting language...", end=" ")
        is_russian = ('russian' in pdf_file.lower() or 
                      'ру' in pdf_file.lower() or
                      detect_russian_content(pdf_text))
        
        if not is_russian:
            print("🇬🇧 English")
        
        # Analyze with LLM
        print("🧠 Analyzing with LLM...", end=" ")
        analysis = analyze_full_paper(pdf_text, pdf_file, client, is_russian=is_russian)
        
        if analysis is None:
            print("❌ Failed")
            continue
        
        print("✅")
        
        extraction_result = {
            "filename": pdf_file,
            "is_russian": is_russian,
            "num_pages": num_pages,
            "text_length": len(pdf_text),
            "analysis": analysis,
            "extracted_at": datetime.now().isoformat()
        }
        
        all_extractions.append(extraction_result)
        
        # Print preview
        print("\n📋 EXTRACTION PREVIEW (first 500 chars):\n")
        print(analysis[:500])
        print("\n... [see full analysis in saved file] ...\n")
        
        time.sleep(1)
    
    print(f"\n{'='*80}")
    print(f"✅ Extracted from {len(all_extractions)} papers")
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"full_paper_extractions_{timestamp}.json"
    save_results(all_extractions, filename)
    
    # Create summary report
    print(f"\n{'='*80}")
    print("📊 CREATING SUMMARY REPORT\n")
    
    report = f"""
{'='*80}
FULL PAPER EXTRACTION - SUMMARY REPORT
{'='*80}

Papers Analyzed: {len(all_extractions)}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{'='*80}
PAPERS PROCESSED:
{'='*80}

"""
    
    for i, extraction in enumerate(all_extractions, 1):
        lang = "🇷🇺 Russian" if extraction['is_russian'] else "🇬🇧 English"
        report += f"\n{i}. {extraction['filename']} ({lang})\n"
        report += f"   Pages: {extraction['num_pages']}\n"
        report += f"   Text Length: {extraction['text_length']} characters\n"
        report += f"   Analysis:\n"
        
        # Add first part of analysis to report
        analysis_lines = extraction['analysis'].split('\n')[:20]
        for line in analysis_lines:
            report += f"   {line}\n"
        report += f"\n   ... [see detailed extraction] ...\n"
    
    report += f"\n{'='*80}\nAll detailed extractions saved to: data/processed/{filename}\n"
    
    print(report)
    
    # Save report
    report_filename = f"full_paper_summary_{timestamp}.txt"
    report_path = os.path.join("data/processed", report_filename)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"💾 Report saved to: {report_path}")
    
    print(f"\n{'='*80}")
    print("✅ FULL PAPER EXTRACTION COMPLETE!")
    print(f"\nNext: Review extractions in data/processed/{filename}")

if __name__ == "__main__":
    main()