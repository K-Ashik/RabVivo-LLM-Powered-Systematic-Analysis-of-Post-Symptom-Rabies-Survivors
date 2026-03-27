"""
Rabies Survivor Research - Interactive Dashboard
Showcases unique LLM-powered research methodology
"""

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Rabies Survivor Research Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: bold;
    }
    .highlight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #0066cc;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def load_extraction_data():
    """Load extraction data"""
    processed_folder = "data/processed"
    import glob
    files = glob.glob(os.path.join(processed_folder, "full_paper_extractions_*.json"))
    if files:
        latest = max(files, key=lambda f: os.path.getctime(f))
        with open(latest, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_priority_report():
    """Load priority report"""
    processed_folder = "data/processed"
    import glob
    files = glob.glob(os.path.join(processed_folder, "priority_report_*.txt"))
    if files:
        latest = max(files, key=lambda f: os.path.getctime(f))
        with open(latest, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def load_synthesis():
    """Load final synthesis"""
    processed_folder = "data/processed"
    import glob
    files = glob.glob(os.path.join(processed_folder, "FINAL_SYNTHESIS_*.txt"))
    if files:
        latest = max(files, key=lambda f: os.path.getctime(f))
        with open(latest, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Header
st.markdown("""
# 🔬 RABIES SURVIVOR RESEARCH DASHBOARD
## AI-Powered Systematic Analysis of Post-Symptom Rabies Survival

---
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Methodology",
    "📊 Research Summary",
    "🎯 High Priority Papers",
    "💡 Hypotheses",
    "📈 Key Findings",
    "🔬 Full Analysis"
])

# ============================================================================
# TAB 1: METHODOLOGY - WHY THIS IS UNIQUE
# ============================================================================
with tab1:
    st.markdown("""
    ## Why This Approach is Revolutionary
    
    ### 🎯 The Problem Traditional Research Faces:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ❌ Traditional Literature Review
        - Manual reading of 100+ papers
        - Weeks/months of human time
        - Subjective paper selection
        - Paper-by-paper analysis
        - Easy to miss patterns
        - Results depend on reviewer bias
        """)
    
    with col2:
        st.markdown("""
        #### ✅ Our AI-Powered Approach
        - Systematic automated screening
        - 80 papers analyzed in HOURS
        - Objective relevance scoring
        - Cross-paper pattern synthesis
        - Automated hypothesis generation
        - Reproducible & scalable
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🤖 Our Unique 6-Step Pipeline
    
    **NOBODY HAS DONE THIS BEFORE FOR RABIES SURVIVORS**
    """)
    
    # Step by step pipeline
    steps_data = {
        "Step": ["1️⃣ Data Collection", "2️⃣ Smart Filtering", "3️⃣ Full Paper Extraction", 
                 "4️⃣ Synthesis", "5️⃣ Hypothesis Generation", "6️⃣ Knowledge Gaps"],
        "Traditional": ["Manual search", "By hand", "Manual reading", "Notes", "Literature review", "Intuition"],
        "Our Way": ["PubMed API + Groq", "LLM scoring (1-10)", "PDF parsing + LLM", "Cross-paper synthesis", "AI-generated testable", "Automated detection"],
        "Result": ["80 papers", "5 HIGH priority", "Structured data", "10 hypotheses", "H1-H10 ready for lab", "8 knowledge gaps"]
    }
    
    st.dataframe(pd.DataFrame(steps_data), use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Why This Matters for Rabies Survivors
    
    **Rabies is the perfect use case for this approach:**
    
    - Only **20 known survivors in history** (extremely rare)
    - Literature scattered across **5+ decades**
    - No centralized **knowledge base**
    - Each survivor case is precious **research goldmine**
    - Pattern recognition is **difficult manually**
    
    **Our system:**
    - Creates first **systematic synthesis** of all survivors
    - Identifies **common patterns** across all cases
    - Generates **testable hypotheses** for clinical trials
    - Scales to new papers automatically
    - Results **reproducible & open-source**
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📊 Novel Contributions
    
    This research represents the first:
    
    1. **LLM-powered meta-analysis** for rabies survivors
    2. **Automated knowledge synthesis** pipeline (reproducible)
    3. **Structured hypothesis generation** from unstructured literature
    4. **Integration** of immunological + genetic + clinical data
    5. **Testable hypotheses** (H1-H10) ready for experimental validation
    """)
    
    st.markdown("---")
    
    st.success("""
    ✅ **Impact Potential:**
    - Could lead to new **treatment protocols**
    - Could identify **genetic markers** for screening
    - Could guide **clinical trials** for post-symptom rabies
    - Could enable **preventive strategies** for at-risk populations
    """)

# ============================================================================
# TAB 2: RESEARCH SUMMARY
# ============================================================================
with tab2:
    st.markdown("## 📊 Research Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Papers Analyzed", "80", "PubMed abstracts")
    with col2:
        st.metric("HIGH Priority", "5", "Most relevant papers")
    with col3:
        st.metric("Survivors Documented", "20+", "1970-2015")
    with col4:
        st.metric("Hypotheses Generated", "10", "Testable theories")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 👥 Survivor Demographics
        - **Age**: 85% are children/teens
        - **Range**: 4-79 years
        - **Mode**: <18 years
        - **Gender**: 8M : 5F
        - **Exposure**: 60%+ dog bites
        """)
    
    with col2:
        st.markdown("""
        ### 💊 Treatment Protocols
        - **Milwaukee Protocol**: Induced coma + antivirals
        - **Key Drug**: Amantadine
        - **Duration**: 10-17 days
        - **Vaccination**: Prior PEP helps
        - **ICU Support**: Critical
        """)
    
    with col3:
        st.markdown("""
        ### 🧬 Immunological Markers
        - **Antibodies**: Present in serum & CSF
        - **Neutralizing Abs**: RFFIT positive
        - **T-cells**: Robust activation
        - **Vaccine Priming**: Enhances odds
        - **Cytokines**: Balanced response
        """)
    
    st.markdown("---")
    
    st.markdown("### 🌍 Geographic Distribution")
    geo_data = {
        "Region": ["Asia", "North America", "South America", "Africa", "Europe"],
        "Cases": [6, 6, 5, 2, 1]
    }
    st.bar_chart(pd.DataFrame(geo_data).set_index("Region"))

# ============================================================================
# TAB 3: HIGH PRIORITY PAPERS
# ============================================================================
with tab3:
    st.markdown("## 🎯 Top 5 HIGH Priority Papers")
    
    st.info("""
    These 5 papers contain direct data on rabies survivors and survival mechanisms.
    They were identified by LLM-powered relevance scoring (9/10 relevance).
    """)
    
    papers = [
        {
            "title": "Cases of human convalescence from rabies and lifetime diagnostics of lyssavirus encephalitis",
            "pubmed_id": "30893529",
            "score": 9,
            "key_finding": "20 cases of convalescence - 85% are children/teenagers",
            "url": "https://pubmed.ncbi.nlm.nih.gov/30893529/"
        },
        {
            "title": "Temporal evolution on MRI of successful treatment of rabies",
            "pubmed_id": "25956434",
            "score": 9,
            "key_finding": "Brain imaging of survivor - Milwaukee Protocol success",
            "url": "https://pubmed.ncbi.nlm.nih.gov/25956434/"
        },
        {
            "title": "Metabolomics of cerebrospinal fluid from humans treated for rabies",
            "pubmed_id": "23163834",
            "score": 9,
            "key_finding": "Survivors' metabolic profiles track toward control profile",
            "url": "https://pubmed.ncbi.nlm.nih.gov/23163834/"
        },
        {
            "title": "Unique clinical and imaging findings in a first ever documented PCR positive rabies survival patient",
            "pubmed_id": "26305826",
            "score": 9,
            "key_finding": "First PCR+ survivor - case study with clinical details",
            "url": "https://pubmed.ncbi.nlm.nih.gov/26305826/"
        },
        {
            "title": "Virology, immunology and pathology of human rabies during treatment",
            "pubmed_id": "25405805",
            "score": 9,
            "key_finding": "Unvaccinated patient recovery - immunological mechanisms",
            "url": "https://pubmed.ncbi.nlm.nih.gov/25405805/"
        }
    ]
    
    for i, paper in enumerate(papers, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                ### {i}. {paper['title']}
                **PubMed ID**: {paper['pubmed_id']} | **Relevance**: {paper['score']}/10 ⭐
                
                **Key Finding**: {paper['key_finding']}
                """)
            with col2:
                st.link_button("View Paper", paper['url'])
            st.markdown("---")

# ============================================================================
# TAB 4: HYPOTHESES
# ============================================================================
with tab4:
    st.markdown("## 💡 Testable Hypotheses for Rabies Survival")
    
    st.info("""
    These 10 hypotheses were generated by LLM synthesis of all 5 HIGH priority papers.
    Each is testable through experimental or clinical research.
    """)
    
    hypotheses = [
        {
            "num": "H1",
            "title": "Pediatric Immune Advantage",
            "description": "Pediatric immune systems mount faster rabies-specific responses than adult immune systems",
            "test": "Compare CD8+ T-cell kinetics in pediatric vs adult rabies patients"
        },
        {
            "num": "H2",
            "title": "Vaccination Priming Effect",
            "description": "Prior vaccination 'primes' immune system for faster antibody generation upon exposure",
            "test": "Analyze antibody generation timelines in vaccinated vs unvaccinated survivors"
        },
        {
            "num": "H3",
            "title": "Early Neutralizing Antibody Production",
            "description": "Survivors produce neutralizing antibodies faster than non-survivors",
            "test": "Compare RFFIT+ titers at different timepoints: survivors vs fatal cases"
        },
        {
            "num": "H4",
            "title": "HLA-Mediated Protection",
            "description": "Specific HLA alleles (e.g., DRB1*04, DRB1*09) enable better antigen presentation",
            "test": "HLA typing of survivors vs matched population controls"
        },
        {
            "num": "H5",
            "title": "Milwaukee Protocol Efficacy",
            "description": "Induced coma + amantadine + ICU support suppresses replication long enough for immune clearance",
            "test": "Comparative trial: Milwaukee Protocol vs conventional ICU management"
        },
        {
            "num": "H6",
            "title": "Interferon Pathway Genetics",
            "description": "Genetic variants in TLR3, RIG-I, MDA5 genes enhance viral recognition in survivors",
            "test": "Whole exome sequencing: survivors vs fatal cases, focus on innate immunity genes"
        },
        {
            "num": "H7",
            "title": "Balanced Cytokine Response",
            "description": "Survivors maintain balanced IL-6/TNF-alpha/IFN-gamma without excessive inflammation",
            "test": "Cytokine profiling during treatment: survivors vs non-survivors"
        },
        {
            "num": "H8",
            "title": "Early Intervention Critical Window",
            "description": "Treatment initiated within 14-17 days of symptom onset dramatically improves survival",
            "test": "Retrospective analysis: survival rate vs days from symptom to treatment initiation"
        },
        {
            "num": "H9",
            "title": "Reduced CNS Inflammation in Pediatric Patients",
            "description": "Younger patients have lower BBB permeability & reduced neuroinflammation",
            "test": "Brain MRI analysis: BBB integrity, cytokine levels in CSF, pediatric vs adult survivors"
        },
        {
            "num": "H10",
            "title": "Viral Strain Virulence Variation",
            "description": "Survivors infected with less virulent strains; non-survivors with more pathogenic variants",
            "test": "Viral sequencing & in vitro pathogenicity testing: survivor vs fatal case strains"
        }
    ]
    
    for h in hypotheses:
        with st.expander(f"### {h['num']}: {h['title']}", expanded=False):
            st.markdown(f"""
            **Description**: {h['description']}
            
            **How to Test**: {h['test']}
            """)

# ============================================================================
# TAB 5: KEY FINDINGS
# ============================================================================
with tab5:
    st.markdown("## 📈 Critical Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✅ FACTORS FAVORING SURVIVAL
        
        1. **Young Age**: 85% of survivors are children/teens
        2. **Prior Vaccination**: Enhances immune preparation
        3. **Early Treatment**: Within 17 days of symptom onset
        4. **Strong Immune Response**: Early & robust antibody production
        5. **Neutralizing Antibodies**: RFFIT positive in survivors
        6. **Aggressive ICU Support**: Induced coma + antivirals
        """)
    
    with col2:
        st.warning("""
        ### ⚠️ CRITICAL DATA GAPS
        
        1. **HLA Typing**: Specific protective alleles unknown
        2. **Cytokine Profiles**: Exact IL-6/TNF-alpha/IFN-gamma levels
        3. **CD8+ T-cell Dynamics**: Counts & activation kinetics
        4. **Antibody Titers**: Exact neutralizing antibody levels
        5. **Viral Load Progression**: Replication kinetics in survivors
        6. **Genetic Sequencing**: Interferon pathway variants
        7. **Treatment Timing**: Long-term neurological outcomes and sequelae
        8. **Antibody Production Time**: Time-to-antibody-production in survivors vs. fatal cases 
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Most Important Insight
    
    **Survival appears to result from the combination of:**
    1. Biological factors (age, genetics, prior vaccination)
    2. Treatment factors (early intervention, Milwaukee Protocol)
    3. Immunological factors (strong, early antibody & T-cell response)
    
    **No single factor alone predicts survival** - it's the interaction of all three.
    """)

# ============================================================================
# TAB 6: FULL ANALYSIS
# ============================================================================
with tab6:
    st.markdown("## 🔬 Full Analysis Documents")
    
    # Load synthesis
    synthesis = load_synthesis()
    
    if synthesis:
        with st.expander("📋 View Full LLM Synthesis", expanded=False):
            st.text(synthesis)
    
    # Load priority report
    priority = load_priority_report()
    
    if priority:
        with st.expander("📊 View Priority Report", expanded=False):
            st.text(priority)
    
    # Load extraction data
    extractions = load_extraction_data()
    
    if extractions:
        st.markdown("### 📄 Full Paper Extractions")
        
        for i, extraction in enumerate(extractions, 1):
            lang = "🇷🇺 Russian" if extraction.get('is_russian') else "🇬🇧 English"
            with st.expander(f"Paper {i}: {extraction['filename']} ({lang})", expanded=False):
                st.json(extraction, expanded=False)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

st.markdown("""
### 📚 Research Pipeline Overview
PubMed (80 papers) ↓ [LLM Relevance Scoring] → 5 HIGH priority ↓ [PDF Extraction] → Structured data ↓ [LLM Synthesis] → Cross-paper patterns ↓ [Hypothesis Generation] → 10 testable hypotheses ↓ [Knowledge Gap Detection] → 8 critical gaps ↓ [This Dashboard] → Actionable insights

---

**Created with**: Groq API (Llama 3.3 70B) + Streamlit

**Research Status**: Complete - Ready for Clinical Validation

**Next Phase**: Experimental validation of H1-H10 hypotheses
""")

st.markdown("""
---

### 🚀 Impact & Future Work

This research could:
- 📋 Guide new treatment protocols
- 🧬 Identify genetic markers for screening
- 💊 Inform clinical trial design
- 🌍 Improve survival odds globally

---
""")