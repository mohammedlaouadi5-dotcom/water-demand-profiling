"""
Extract detailed citations from Undermind PDF report
This PDF likely contains a comprehensive list of recent papers
"""
import PyPDF2
from pathlib import Path
import re

pdf_path = r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\Undermind - Survey-informed residential water end-use disaggregation segmentation and leak detection methods.pdf"

print("="*100)
print("EXTRACTING UNDERMIND LITERATURE SEARCH REPORT")
print("="*100)

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        print(f"\nTotal pages: {total_pages}")
        print("\n" + "="*100)
        
        full_text = ""
        for i in range(total_pages):
            page_text = reader.pages[i].extract_text()
            full_text += page_text + "\n\n"
            print(f"Page {i+1}/{total_pages} extracted ({len(page_text)} chars)")
        
        # Save full text
        output_file = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\undermind_full_text.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("UNDERMIND LITERATURE SEARCH - FULL TEXT EXTRACTION\n")
            f.write("="*100 + "\n\n")
            f.write(full_text)
        
        print(f"\n✓ Full text saved to: {output_file}")
        
        # Extract potential citations
        print("\n" + "="*100)
        print("SEARCHING FOR CITATIONS")
        print("="*100)
        
        # Look for year patterns (2015-2025)
        years = re.findall(r'\b(20[12]\d)\b', full_text)
        year_counts = {}
        for year in years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print("\n📅 Year distribution:")
        for year in sorted(year_counts.keys(), reverse=True):
            print(f"  {year}: {year_counts[year]} mentions")
        
        # Look for DOI patterns
        dois = re.findall(r'10\.\d{4,}/[^\s,;]+', full_text)
        print(f"\n📚 Found {len(set(dois))} unique DOIs")
        
        # Look for author patterns (Name et al.)
        author_patterns = re.findall(r'\b[A-Z][a-z]+ et al\.', full_text)
        print(f"\n👥 Found {len(set(author_patterns))} unique 'et al.' citations")
        
        # Extract first 5000 characters to see structure
        print("\n" + "="*100)
        print("FIRST 5000 CHARACTERS OF DOCUMENT")
        print("="*100)
        print(full_text[:5000])
        
        # Try to find title/journal patterns
        print("\n" + "="*100)
        print("SEARCHING FOR JOURNAL NAMES")
        print("="*100)
        
        journal_patterns = [
            r'Water Research',
            r'Water Resources Research',
            r'Journal of [\w\s]+',
            r'Environmental Science',
            r'Resources, Conservation',
            r'Applied Energy',
            r'Energy and Buildings'
        ]
        
        found_journals = []
        for pattern in journal_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            if matches:
                found_journals.extend(matches)
        
        print(f"Found {len(set(found_journals))} journal mentions:")
        for journal in sorted(set(found_journals))[:20]:
            print(f"  • {journal}")
        
        # Look for paper titles (lines with multiple capitalized words)
        print("\n" + "="*100)
        print("POTENTIAL PAPER TITLES (First 20)")
        print("="*100)
        
        lines = full_text.split('\n')
        potential_titles = []
        for line in lines:
            line = line.strip()
            # Title pattern: starts with capital, contains multiple words, 20-150 chars
            if (len(line) > 20 and len(line) < 150 and 
                line[0].isupper() and 
                sum(1 for c in line if c.isupper()) > 3):
                potential_titles.append(line)
        
        for i, title in enumerate(potential_titles[:20], 1):
            print(f"{i}. {title}")
        
        print(f"\n✓ Total potential titles found: {len(potential_titles)}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*100)
print("EXTRACTION COMPLETE")
print("="*100)
