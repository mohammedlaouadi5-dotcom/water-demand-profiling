"""
Extract citation information from PDF files in the workspace
"""
import os
import re
from pathlib import Path

# Try different PDF libraries
try:
    import PyPDF2
    pdf_lib = "PyPDF2"
except ImportError:
    pdf_lib = None

try:
    import pdfplumber
    pdf_lib = "pdfplumber"
except ImportError:
    pass

def extract_text_pypdf2(pdf_path):
    """Extract text using PyPDF2"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            # Extract first 5 pages for title, abstract, intro
            for i in range(min(5, len(reader.pages))):
                text += reader.pages[i].extract_text()
            return text
    except Exception as e:
        return f"Error with PyPDF2: {e}"

def extract_text_pdfplumber(pdf_path):
    """Extract text using pdfplumber"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            # Extract first 5 pages
            for i in range(min(5, len(pdf.pages))):
                text += pdf.pages[i].extract_text()
        return text
    except Exception as e:
        return f"Error with pdfplumber: {e}"

def extract_metadata(text, filename):
    """Extract title, authors, year from text"""
    metadata = {
        'filename': filename,
        'title': '',
        'authors': '',
        'year': '',
        'abstract_snippet': ''
    }
    
    # Try to find year (4-digit number likely in citation range)
    year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', text[:1000])
    if year_match:
        metadata['year'] = year_match.group(1)
    
    # Extract first 500 chars for title/abstract
    lines = text[:1000].split('\n')
    non_empty = [l.strip() for l in lines if l.strip()]
    if non_empty:
        metadata['title'] = non_empty[0][:200]
    
    # Look for abstract
    abstract_match = re.search(r'abstract[:\s]+(.{0,500})', text[:3000], re.IGNORECASE)
    if abstract_match:
        metadata['abstract_snippet'] = abstract_match.group(1).strip()[:300]
    
    return metadata

# Main execution
workspace_dir = Path(r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling')
pdf_files = list(workspace_dir.glob('*.pdf'))

print(f"Found {len(pdf_files)} PDF files")
print(f"Using library: {pdf_lib}")
print("="*80)

results = []

for pdf_file in pdf_files:
    print(f"\nProcessing: {pdf_file.name}")
    print("-" * 80)
    
    if pdf_lib == "pdfplumber":
        text = extract_text_pdfplumber(pdf_file)
    elif pdf_lib == "PyPDF2":
        text = extract_text_pypdf2(pdf_file)
    else:
        print("No PDF library available. Install PyPDF2 or pdfplumber")
        break
    
    if text and not text.startswith("Error"):
        metadata = extract_metadata(text, pdf_file.name)
        results.append(metadata)
        
        print(f"Title: {metadata['title']}")
        print(f"Year: {metadata['year']}")
        print(f"Abstract: {metadata['abstract_snippet'][:150]}...")
    else:
        print(f"Failed to extract: {text}")

# Save results
print("\n" + "="*80)
print("SUMMARY OF EXTRACTED PAPERS:")
print("="*80)

for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['filename']}")
    print(f"   Year: {result['year']}")
    print(f"   Title: {result['title'][:100]}...")

# Write to file
output_file = workspace_dir / 'literature_extraction.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("LITERATURE REVIEW PDF EXTRACTION\n")
    f.write("="*80 + "\n\n")
    
    for i, result in enumerate(results, 1):
        f.write(f"{i}. {result['filename']}\n")
        f.write(f"   Year: {result['year']}\n")
        f.write(f"   Title: {result['title']}\n")
        f.write(f"   Abstract: {result['abstract_snippet']}\n")
        f.write("\n" + "-"*80 + "\n\n")

print(f"\nResults saved to: {output_file}")
