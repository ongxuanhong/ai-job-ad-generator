import os
import tempfile
import unittest
import fitz  # PyMuPDF
import docx

from scripts.extract_text import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extract_text_from_file,
    extract_text_from_folder,
)


class TestExtractTextFunctions(unittest.TestCase):
    def _create_temp_pdf(
        self, text: str, temp_dir: str, filename: str = "test.pdf"
    ) -> str:
        """Creates a temporary PDF file with the given text."""
        pdf_path = os.path.join(temp_dir, filename)
        doc = fitz.open()  # create a new PDF in memory
        page = doc.new_page()  # add a page
        # Insert text at a fixed position
        page.insert_text((72, 72), text)
        doc.save(pdf_path)
        doc.close()
        return pdf_path

    def _create_temp_docx(
        self, paragraphs: list, temp_dir: str, filename: str = "test.docx"
    ) -> str:
        """Creates a temporary DOCX file with the given paragraphs."""
        docx_path = os.path.join(temp_dir, filename)
        document = docx.Document()
        for para in paragraphs:
            document.add_paragraph(para)
        document.save(docx_path)
        return docx_path

    def _create_temp_txt(
        self, text: str, temp_dir: str, filename: str = "test.txt"
    ) -> str:
        """Creates a temporary TXT file with the given text."""
        txt_path = os.path.join(temp_dir, filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        return txt_path

    def test_extract_text_from_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Prepare sample text with two paragraphs separated by a double newline.
            sample_text = "PDF Paragraph 1\nPDF Paragraph 2"
            pdf_path = self._create_temp_pdf(sample_text, temp_dir)
            paragraphs = extract_text_from_pdf(pdf_path)
            self.assertIsInstance(paragraphs, list)
            # The extraction splits text on double newlines.
            self.assertEqual(paragraphs, [sample_text])

    def test_extract_text_from_docx(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paragraphs_input = ["DOCX Paragraph 1", "DOCX Paragraph 2"]
            docx_path = self._create_temp_docx(paragraphs_input, temp_dir)
            paragraphs = extract_text_from_docx(docx_path)
            self.assertIsInstance(paragraphs, list)
            self.assertEqual(paragraphs, paragraphs_input)

    def test_extract_text_from_txt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_text = "TXT Paragraph 1\n\nTXT Paragraph 2"
            txt_path = self._create_temp_txt(sample_text, temp_dir)
            paragraphs = extract_text_from_txt(txt_path)
            self.assertIsInstance(paragraphs, list)
            self.assertEqual(paragraphs, ["TXT Paragraph 1", "TXT Paragraph 2"])

    def test_extract_text_from_file_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_text = "PDF File Paragraph 1\nPDF File Paragraph 2"
            pdf_path = self._create_temp_pdf(
                sample_text, temp_dir, filename="sample.pdf"
            )
            result = extract_text_from_file(pdf_path)
            self.assertIsInstance(result, dict)
            self.assertEqual(result["file_name"], "sample.pdf")
            self.assertEqual(result["paragraphs"], [sample_text])

    def test_extract_text_from_file_docx(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paragraphs_input = ["DOCX File Paragraph 1", "DOCX File Paragraph 2"]
            docx_path = self._create_temp_docx(
                paragraphs_input, temp_dir, filename="sample.docx"
            )
            result = extract_text_from_file(docx_path)
            self.assertIsInstance(result, dict)
            self.assertEqual(result["file_name"], "sample.docx")
            self.assertEqual(result["paragraphs"], paragraphs_input)

    def test_extract_text_from_file_txt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_text = "TXT File Paragraph 1\n\nTXT File Paragraph 2"
            txt_path = self._create_temp_txt(
                sample_text, temp_dir, filename="sample.txt"
            )
            result = extract_text_from_file(txt_path)
            self.assertIsInstance(result, dict)
            self.assertEqual(result["file_name"], "sample.txt")
            self.assertEqual(
                result["paragraphs"], ["TXT File Paragraph 1", "TXT File Paragraph 2"]
            )

    def test_extract_text_from_file_unsupported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            unsupported_path = os.path.join(temp_dir, "unsupported.csv")
            with open(unsupported_path, "w", encoding="utf-8") as f:
                f.write("Unsupported, file, content")
            with self.assertRaises(ValueError):
                extract_text_from_file(unsupported_path)

    def test_extract_text_from_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create one PDF, one DOCX, one TXT and one unsupported file in the same folder.
            pdf_text = "Folder PDF Paragraph\n\nAnother Folder PDF Paragraph"
            docx_paragraphs = ["Folder DOCX Paragraph 1", "Folder DOCX Paragraph 2"]
            txt_text = "Folder TXT Paragraph 1\n\nFolder TXT Paragraph 2"

            pdf_path = self._create_temp_pdf(pdf_text, temp_dir, filename="file.pdf")
            docx_path = self._create_temp_docx(
                docx_paragraphs, temp_dir, filename="file.docx"
            )
            txt_path = self._create_temp_txt(txt_text, temp_dir, filename="file.txt")

            # Create an unsupported file (this should be ignored by the extraction function).
            unsupported_path = os.path.join(temp_dir, "ignore.csv")
            with open(unsupported_path, "w", encoding="utf-8") as f:
                f.write("ignore this file")

            results = extract_text_from_folder(temp_dir)
            # Expecting three files (PDF, DOCX, TXT) to be processed.
            self.assertEqual(len(results), 3)

            # Check that the returned dictionaries have the expected file names.
            returned_file_names = {result["file_name"] for result in results}
            expected_file_names = {"file.pdf", "file.docx", "file.txt"}
            self.assertEqual(returned_file_names, expected_file_names)


if __name__ == "__main__":
    unittest.main()
