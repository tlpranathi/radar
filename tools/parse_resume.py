from pathlib import Path
from pypdf import PdfReader
from docx import Document


def parse_resume(file_path: str) -> str:
    """
    Extract text from a PDF or DOCX resume.

    Args:
        file_path: Path to the resume file.

    Returns:
        Extracted resume text as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the format is unsupported or no text is extracted.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        resume_text = "\n".join(text_parts)

    elif suffix == ".docx":
        document = Document(str(path))

        text_parts = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        # also extract text from tables, which resumes often use
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_parts.append(cell.text)

        resume_text = "\n".join(text_parts)

    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Use PDF or DOCX."
        )

    resume_text = resume_text.strip()

    if not resume_text:
        raise ValueError(
            "No text could be extracted. The resume may be empty "
            "or the PDF may contain scanned images."
        )

    return resume_text