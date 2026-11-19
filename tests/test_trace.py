import unittest
from detection.trace import TraceRecord
class TestTraceRecord(unittest.TestCase):

    def test_create_trace(self):
        trace = TraceRecord(
            source="query_parameter",
            source_location='request.args["name"]',
            variable="user_input"
        )

        self.assertEqual(trace.source, "query_parameter")
        self.assertEqual(trace.variable, "user_input")
        self.assertEqual(trace.context, "unknown")

    def test_add_flow_step(self):
        trace = TraceRecord(
            source="form_parameter",
            source_location='request.form["comment"]',
            variable="comment"
        )

        trace.add_flow_step("Assigned to comment variable")

        self.assertEqual(
            trace.flow_steps,
            ["Assigned to comment variable"]
        )

    def test_multiple_flow_steps(self):
        trace = TraceRecord(
            source="query_parameter",
            source_location='request.args["q"]',
            variable="user_input"
        )

        trace.add_flow_step("Assigned to variable")
        trace.add_flow_step("Passed to formatting function")

        self.assertEqual(len(trace.flow_steps), 2)

    def test_sink_information(self):
        trace = TraceRecord(
            source="query_parameter",
            source_location='request.args["q"]',
            variable="user_input",
            sink="html_response",
            sink_location="result.html",
            context="html_text"
        )

        self.assertEqual(trace.sink, "html_response")
        self.assertEqual(trace.context, "html_text")

    def test_empty_flow_step(self):
        trace = TraceRecord(
            source="query_parameter",
            source_location='request.args["q"]',
            variable="user_input"
        )

        with self.assertRaises(ValueError):
            trace.add_flow_step("")

if __name__ == "__main__":
    unittest.main()
