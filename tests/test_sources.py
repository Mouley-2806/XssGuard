import unittest
from flask import Flask, request
from detection.sources import extract_request_sources, create_input_traces

class TestInputSources(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    def test_query_parameter(self):
        with self.app.test_request_context("/?name=test"):
            sources = extract_request_sources(request)

        self.assertTrue(
            any(source.source_type == "query"
                for source in sources)
        )

    def test_query_input_creates_trace(self):
        with self.app.test_request_context("/?search=hello"):
            traces = create_input_traces(request)

        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0].source, "query")
        self.assertEqual(traces[0].variable, "search")

    def test_form_parameter(self):
        with self.app.test_request_context(
            "/", method="POST", data={"username": "test"}
        ):
            sources = extract_request_sources(request)

        self.assertTrue(
            any(source.source_type == "form"
                for source in sources)
        )

if __name__ == "__main__":
    unittest.main()
