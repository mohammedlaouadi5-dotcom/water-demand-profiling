"""
Deep extraction of academic papers from PDFs for literature review
"""
import PyPDF2
from pathlib import Path
import re

def extract_full_text(pdf_path, max_pages=10):
    """Extract text from PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for i in range(min(max_pages, len(reader.pages))):
                text += reader.pages[i].extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error: {e}"

def extract_paper_info(text, filename):
    """Extract detailed paper information"""
    info = {
        'filename': filename,
        'title': '',
        'authors': '',
        'year': '',
        'journal': '',
        'doi': '',
        'keywords': [],
        'abstract': '',
        'conclusion': '',
        'methods': []
    }
    
    # Extract year
    year_patterns = [
        r'\b(20[0-2]\d)\b',  # 2000-2029
        r'\((\d{4})\)',      # (2019)
    ]
    for pattern in year_patterns:
        match = re.search(pattern, text[:2000])
        if match:
            year = match.group(1)
            if 2000 <= int(year) <= 2025:
                info['year'] = year
                break
    
    # Extract DOI
    doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', text[:3000])
    if doi_match:
        info['doi'] = doi_match.group(1).rstrip('.,;')
    
    # Extract title (usually first non-empty line or large text)
    lines = [l.strip() for l in text[:1500].split('\n') if l.strip() and len(l.strip()) > 10]
    if lines:
        # Find longest line in first 10 lines (likely title)
        potential_titles = lines[:10]
        info['title'] = max(potential_titles, key=len)[:250]
    
    # Extract abstract
    abstract_pattern = r'abstract[:\s]+(.*?)(?=introduction|keywords|1\.|methods|background|\n\n\d+\.|$)'
    abstract_match = re.search(abstract_pattern, text[:5000], re.IGNORECASE | re.DOTALL)
    if abstract_match:
        info['abstract'] = abstract_match.group(1).strip()[:800]
    
    # Extract keywords
    keywords_pattern = r'keywords[:\s]+(.*?)(?=\n\n|\d+\.|introduction|background)'
    keywords_match = re.search(keywords_pattern, text[:5000], re.IGNORECASE | re.DOTALL)
    if keywords_match:
        keywords_text = keywords_match.group(1).strip()
        info['keywords'] = [k.strip() for k in re.split(r'[;,\n]', keywords_text) if k.strip()][:10]
    
    # Look for methodology keywords
    method_keywords = [
        'clustering', 'machine learning', 'GMM', 'Gaussian Mixture',
        'bootstrap', 'feature selection', 'k-means', 'hierarchical',
        'random forest', 'neural network', 'deep learning',
        'SHAP', 'XAI', 'explainable', 'interpretable',
        'water demand', 'smart meter', 'behavioral', 'segmentation',
        'NMF', 'PCA', 'dimensionality reduction'
    ]
    
    for keyword in method_keywords:
        if re.search(keyword, text, re.IGNORECASE):
            info['methods'].append(keyword)
    
    # Extract journal name
    journal_patterns = [
        r'Water Resources Research',
        r'Journal of [\w\s]+',
        r'Resources, Conservation and Recycling',
        r'Environmental Science',
        r'Water Research'
    ]
    for pattern in journal_patterns:
        match = re.search(pattern, text[:3000], re.IGNORECASE)
        if match:
            info['journal'] = match.group(0)
            break
    
    return info

# Process PDFs
workspace_dir = Path(r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling')
pdf_files = sorted(workspace_dir.glob('*.pdf'))

print("="*100)
print("DETAILED PDF LITERATURE EXTRACTION")
print("="*100)

all_papers = []

for pdf_file in pdf_files:
    print(f"\n{'='*100}")
    print(f"Processing: {pdf_file.name}")
    print('='*100)
    
    text = extract_full_text(pdf_file, max_pages=15)
    
    if not text.startswith("Error"):
        info = extract_paper_info(text, pdf_file.name)
        all_papers.append(info)
        
        print(f"\n✓ TITLE: {info['title']}")
        print(f"✓ YEAR: {info['year']}")
        print(f"✓ JOURNAL: {info['journal']}")
        print(f"✓ DOI: {info['doi']}")
        print(f"\n✓ KEYWORDS: {', '.join(info['keywords'][:5])}")
        print(f"\n✓ METHODS DETECTED: {', '.join(info['methods'][:8])}")
        print(f"\n✓ ABSTRACT:\n{info['abstract'][:400]}...")
    else:
        print(f"✗ Failed: {text}")

# Generate literature review summary
print("\n\n" + "="*100)
print("LITERATURE REVIEW SUMMARY")
print("="*100)

# Categorize by year
recent_papers = [p for p in all_papers if p['year'] and int(p['year']) >= 2020]
older_papers = [p for p in all_papers if p['year'] and int(p['year']) < 2020]

print(f"\n📊 STATISTICS:")
print(f"  • Total papers: {len(all_papers)}")
print(f"  • Recent (2020-2024): {len(recent_papers)}")
print(f"  • Older (pre-2020): {len(older_papers)}")

# Save detailed report
output_file = workspace_dir / 'literature_detailed_extraction.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("DETAILED LITERATURE EXTRACTION FOR MANUSCRIPT\n")
    f.write("="*100 + "\n\n")
    
    for i, paper in enumerate(all_papers, 1):
        f.write(f"\n{'='*100}\n")
        f.write(f"PAPER {i}\n")
        f.write('='*100 + "\n\n")
        f.write(f"Filename: {paper['filename']}\n")
        f.write(f"Title: {paper['title']}\n")
        f.write(f"Year: {paper['year']}\n")
        f.write(f"Journal: {paper['journal']}\n")
        f.write(f"DOI: {paper['doi']}\n")
        f.write(f"\nKeywords: {', '.join(paper['keywords'])}\n")
        f.write(f"\nMethods: {', '.join(paper['methods'])}\n")
        f.write(f"\nAbstract:\n{paper['abstract']}\n")
        f.write("\n" + "-"*100 + "\n")

print(f"\n✓ Detailed report saved to: {output_file}")

# Generate citation recommendations
print("\n" + "="*100)
print("CITATION RECOMMENDATIONS FOR MANUSCRIPT")
print("="*100)

print("\n📌 RECENT LITERATURE (2020+) TO ADD:")
for paper in recent_papers:
    print(f"\n  • [{paper['year']}] {paper['title'][:80]}...")
    print(f"    Methods: {', '.join(paper['methods'][:5])}")

print("\n📌 BENCHMARK PAPERS (Pre-2020):")
for paper in older_papers:
    print(f"\n  • [{paper['year']}] {paper['title'][:80]}...")
    print(f"    Methods: {', '.join(paper['methods'][:5])}")

print(f"\n{'='*100}\n")
