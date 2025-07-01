import os

def read_file_content(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.pdf':
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text

        # Semua file lain dianggap teks
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    except Exception as e:
        return f"[Error reading file: {e}]"

