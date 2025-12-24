from pypdf import PdfReader

reader = PdfReader(r"\document_path")
print(reader.pages[0].extract_text())
