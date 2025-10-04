import fitz  # PyMuPDF
import sys
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python extract_pdf_text.py <ruta_del_pdf>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    extracted_text = extract_text_from_pdf(pdf_file)
    
    # Create output directory relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "docs", "texts")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get PDF filename without extension and create .txt filename
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = os.path.join(output_dir, f"{pdf_name}.txt")
    
    # Save extracted text to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    print(f"Texto extraído y guardado en: {output_file}")
