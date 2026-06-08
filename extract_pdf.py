import sys

try:
    import pdfplumber
    pdf_path = r'.\AIAP 24 Technical Assessment.pdf'
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF has {len(pdf.pages)} pages\n")
        for i, page in enumerate(pdf.pages):
            print(f"{'='*80}")
            print(f"PAGE {i+1}")
            print(f"{'='*80}")
            text = page.extract_text()
            if text:
                print(text)
            tables = page.extract_tables()
            if tables:
                print("\nTABLES FOUND:")
                for j, table in enumerate(tables):
                    print(f"\nTable {j+1}:")
                    for row in table:
                        print(row)
            print("\n")
            
except ImportError:
    print("pdfplumber not installed. Trying PyPDF2...")
    try:
        from PyPDF2 import PdfReader
        pdf_path = r'.\AIAP 24 Technical Assessment.pdf'
        
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            print(f"PDF has {len(reader.pages)} pages\n")
            for i, page in enumerate(reader.pages):
                print(f"{'='*80}")
                print(f"PAGE {i+1}")
                print(f"{'='*80}")
                print(page.extract_text())
                print("\n")
    except ImportError:
        print("PyPDF2 not installed either.")
        print("Please install one of these:")
        print("  pip install pdfplumber")
        print("  pip install PyPDF2")
        sys.exit(1)
