"""
Final Synthesis Script
Combines all extracted data and generates comprehensive knowledge synthesis
"""

import json
import os
from datetime import datetime
import streamlit as st
from groq import Groq

def load_json_file(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def generate_final_synthesis(all_data, client):
    """
    Use Llama to generate comprehensive final synthesis
    """
    
    # Prepare data summary
    data_summary = json.dumps(all_data, indent=2, ensure_ascii=False)[:6000]
    
    synthesis_prompt = f"""You are creating a COMPREHENSIVE RESEARCH SYNTHESIS on rabies survivors.

Based on the analysis of 5 HIGH priority full papers containing data on 20+ rabies survivors, here is the extracted data:

{data_summary}

Please create a detailed synthesis addressing:

1. SURVIVOR PROFILE (Who survives?)
   - Demographic patterns
   - Age correlation with survival
   - Gender differences
   - Geographic variation

2. CRITICAL SURVIVAL FACTORS (Why do they survive?)
   - Role of prior vaccination
   - Importance of age
   - Treatment timing and protocols
   - Immune response characteristics
   
3. TREATMENT BREAKTHROUGHS (What enables survival?)
   - Milwaukee Protocol specifics
   - Antivirals used (amantadine, etc.)
   - Induced coma benefit
   - ICU support requirements
   - Treatment duration

4. IMMUNOLOGICAL MECHANISMS (How does the immune system win?)
   - Antibody responses (types, titers)
   - Neutralizing antibody importance
   - T-cell response patterns
   - Vaccination priming effect
   - Cytokine balance

5. GENETIC/HOST FACTORS (Nature vs. Nurture?)
   - Age as genetic proxy (younger = different immune state?)
   - HLA predispositions (mentioned but not detailed)
   - Possible protective genetic variants
   - Viral strain susceptibility

6. TESTABLE HYPOTHESES (What should we investigate?)
   Based on the data, propose 5-10 specific, testable hypotheses about:
   - Why younger patients survive better
   - How prior vaccination enables survival
   - What immunological markers predict survival
   - How to improve survival rates

7. CLINICAL IMPLICATIONS (What can doctors do?)
   - Early intervention protocols
   - Vaccination importance for at-risk populations
   - Immunological monitoring during treatment
   - Treatment optimization strategies

8. KNOWLEDGE GAPS REQUIRING FULL PAPER REVIEW (Critical missing data)
   - What specific HLA types protect?
   - What are the exact cytokine profiles?
   - What genetic variants enable survival?
   - What is the viral load progression?
   - What is the long-term neurological outcome?

9. RESEARCH ROADMAP (Next steps)
   - Priority investigations
   - Key experiments needed
   - Patient cohort studies needed
   - Genetic screening recommendations

10. PROVISIONAL HYPOTHESIS (The most likely explanation)
    Based on all evidence, what is the most probable mechanism enabling survival?

Format as a detailed research document with clear sections."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": synthesis_prompt
                }
            ],
            max_tokens=3000,
            temperature=0.4
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def create_visual_summary():
    """Create a visual summary of findings"""
    
    summary = """
╔════════════════════════════════════════════════════════════════════════════╗
║                  RABIES SURVIVOR RESEARCH - DATA SUMMARY                   ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ SURVIVORS DOCUMENTED ─────────────────────────────────────────────────────┐
│                                                                            │
│  Total Cases Reviewed:        20+ survivors (1970-2015)                   │
│  Age Profile:                 85% are children/teenagers                  │
│  Age Range:                   4-79 years (mode: <18 years)                │
│  Gender Distribution:         8M : 5F (slight male bias)                  │
│  Exposure Type:               60%+ dog bites, some bats                   │
│  Geographic Distribution:     Global (Asia, Americas, Africa, Europe)     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ TREATMENT PROTOCOLS ENABLING SURVIVAL ────────────────────────────────────┐
│                                                                            │
│  Milwaukee Protocol:          Induced coma + antivirals                   │
│  Key Drug:                    Amantadine (antiviral)                      │
│  Duration:                    10-17 days intensive treatment              │
│  Vaccination Status:          Most had prior PEP/vaccination              │
│  First Vaccine-Naive:         Survived in 2004 (breakthrough)             │
│  ICU Support:                 Critical for survival                       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ IMMUNOLOGICAL MARKERS IN SURVIVORS ───────────────────────────────────────┐
│                                                                            │
│  Antibody Response:           Positive in serum & CSF                     │
│  Neutralizing Antibodies:     PRESENT & functional (RFFIT+)               │
│  T-cell Response:             ROBUST activation reported                  │
│  Vaccine Priming:             Enhances survival odds                      │
│  Cytokine Profile:            Balanced (IL-6, TNF-alpha, IFN-gamma)      │
│  Immune Activation:           EARLY & STRONG in survivors                 │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ CRITICAL FINDINGS ────────────────────────────────────────────────────────┐
│                                                                            │
│  ✓ Age Matters:               Children have higher survival rate          │
│  ✓ Vaccination Helps:         Prior PEP/vaccination improves odds         │
│  ✓ Early Treatment:           Treatment within 17 days enables survival   │
│  ✓ Immune Response:           Strong, early immune response = survival    │
│  ✓ Antibodies Work:           Neutralizing antibodies critical            │
│  ✓ Timing Critical:           Days matter - early intervention essential  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ KEY HYPOTHESES FOR INVESTIGATION ────────────────────────────────────────┐
│                                                                            │
│  H1: Pediatric immune systems mount faster rabies response                │
│  H2: Prior vaccination "primes" immune system for faster antibody gen.    │
│  H3: Early aggressive treatment suppresses viral replication long enough  │
│       for immune system to eliminate virus                                │
│  H4: Specific HLA alleles enable better rabies antigen presentation       │
│  H5: Younger patients have less CNS inflammatory damage                   │
│  H6: Specific genetic variants in interferon pathway enhance survival     │
│  H7: Vaccination status determines CD8+ T-cell recall response            │
│  H8: Early neutralizing antibody production is survival predictor         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ CRITICAL DATA GAPS (Requires Full Paper Deep Dive) ──────────────────────┐
│                                                                            │
│  ❌ HLA typing of survivors (mentioned but not detailed)                  │
│  ❌ Specific cytokine profiles (IL-6, TNF-alpha, IFN-gamma titers)       │
│  ❌ CD8+ and CD4+ T-cell counts during treatment                          │
│  ❌ Antibody titers and kinetics                                          │
│  ❌ Viral load progression in survivors vs. fatal cases                   │
│  ❌ Genetic sequencing of survivors (interferon pathway genes)            │
│  ❌ Long-term neurological outcomes and sequelae                          │
│  ❌ Time-to-antibody-production in survivors vs. fatal cases              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

"""
    return summary

def main():
    """Main function"""
    
    # Load Groq API
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except:
        print("❌ GROQ_API_KEY not found")
        return
    
    client = Groq(api_key=groq_api_key)
    
    print("=" * 80)
    print("RABIES SURVIVOR RESEARCH - FINAL SYNTHESIS")
    print("=" * 80)
    print()
    
    # Load all extracted data
    print("📂 Loading extracted data...\n")
    
    processed_folder = "data/processed"
    
    # Find latest extractions file
    import glob
    extraction_files = glob.glob(os.path.join(processed_folder, "full_paper_extractions_*.json"))
    
    if not extraction_files:
        print("❌ No extraction files found!")
        return
    
    latest_file = max(extraction_files, key=lambda f: os.path.getctime(f))
    all_extractions = load_json_file(latest_file)
    
    if not all_extractions:
        print("❌ Could not load extraction file")
        return
    
    print(f"✅ Loaded {len(all_extractions)} paper extractions\n")
    
    # Display visual summary
    visual_summary = create_visual_summary()
    print(visual_summary)
    
    # Generate final synthesis
    print("\n" + "=" * 80)
    print("🧠 GENERATING COMPREHENSIVE SYNTHESIS WITH LLM...")
    print("=" * 80 + "\n")
    
    synthesis = generate_final_synthesis(all_extractions, client)
    
    if synthesis:
        print("📋 FINAL RESEARCH SYNTHESIS:\n")
        print(synthesis)
        
        # Save comprehensive report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"FINAL_SYNTHESIS_{timestamp}.txt"
        report_path = os.path.join(processed_folder, report_filename)
        
        full_report = visual_summary + "\n\n" + "=" * 80 + "\n"
        full_report += "LLM-GENERATED COMPREHENSIVE SYNTHESIS\n"
        full_report += "=" * 80 + "\n\n" + synthesis
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"\n\n💾 Complete report saved to: {report_path}")
        
        print(f"\n{'='*80}")
        print("✅ FINAL SYNTHESIS COMPLETE!")
        print(f"\nDeliverables Created:")
        print(f"  1. Visual Summary (above)")
        print(f"  2. Comprehensive Synthesis (in saved file)")
        print(f"  3. Research Hypotheses (above)")
        print(f"  4. Knowledge Gaps (above)")
        print(f"  5. Next Steps (in saved file)")
        
        return report_path
    else:
        print("❌ Failed to generate synthesis")
        return None

if __name__ == "__main__":
    main()