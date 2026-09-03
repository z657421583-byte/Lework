import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from extract_attendance import json_path_for_page_image, prepare_pages


class ExtractAttendanceTest(unittest.TestCase):
    def test_copies_image_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sheet.png"
            source.write_bytes(b"\x89PNG\r\n")
            output = Path(directory) / "pages"
            pages = prepare_pages([source], output)
            self.assertEqual(len(pages), 1)
            self.assertTrue(Path(pages[0]).is_file())
            self.assertEqual(Path(pages[0]).read_bytes(), source.read_bytes())
            payload = json.dumps({"pages": pages})
            self.assertIn("doc-1.png", payload)

    def test_json_path_sits_beside_rendered_png(self):
        png = Path("/tmp/.attendance-pages/doc-1/page-15-part-1.png")
        self.assertEqual(
            json_path_for_page_image(str(png)),
            str(png.with_name("page-15.json")),
        )


if __name__ == "__main__":
    unittest.main()
