import ast
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


class SecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backend = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(cls.backend))
        cls.tmp = tempfile.TemporaryDirectory()
        cls.old_cwd = os.getcwd()
        os.chdir(cls.tmp.name)
        cls.stack = __import__("contextlib").ExitStack()
        cls.stack.enter_context(patch.dict(os.environ, {"FRONTEND_URL": "https://trusted.example"}))
        from types import ModuleType
        for name, symbol in [("services.speech_service", "SpeechService"), ("services.openai_service", "OpenAIService"), ("services.pdf_service", "PDFService")]:
            module = ModuleType(name)
            setattr(module, symbol, Mock())
            cls.stack.enter_context(patch.dict(sys.modules, {name: module}))
        spec = importlib.util.spec_from_file_location("security_test_app", cls.backend / "app.py")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.client = cls.module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.stack.close()
        os.chdir(cls.old_cwd)
        cls.tmp.cleanup()

    def test_untrusted_origin_is_not_authorized(self):
        response = self.client.options('/transcribe', headers={"Origin": "https://untrusted.example", "Access-Control-Request-Method": "POST"})
        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_configured_origin_is_authorized(self):
        response = self.client.options('/transcribe', headers={"Origin": "https://trusted.example", "Access-Control-Request-Method": "POST"})
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "https://trusted.example")
    def test_download_is_limited_to_output_directory(self):
        output = Path(self.module.app.config["OUTPUT_FOLDER"])
        (output / "sample.pdf").write_bytes(b"%PDF-1.4 test")
        Path("outside.pdf").write_bytes(b"private")
        self.assertEqual(self.client.get("/download-pdf/sample.pdf").status_code, 200)
        self.assertEqual(self.client.get("/download-pdf/missing.pdf").status_code, 404)
        self.assertNotEqual(self.client.get("/download-pdf/../outside.pdf").status_code, 200)
        self.assertNotEqual(self.client.get("/download-pdf/%2e%2e%2foutside.pdf").status_code, 200)


if __name__ == "__main__":
    unittest.main()
