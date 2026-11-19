from dataclasses import dataclass
from detection.trace import TraceRecord

@dataclass
class InputSource:
    source_type: str
    name: str
    value: str

def extract_request_sources(request):
    sources = []

    for name, value in request.args.items():
        sources.append(InputSource("query", name, value))

    for name, value in request.form.items():
        sources.append(InputSource("form", name, value))

    for name, value in request.headers.items():
        sources.append(InputSource("header", name, value))

    return sources


def create_input_traces(request):
    traces = []

    sources = extract_request_sources(request)

    for source in sources:
        trace = TraceRecord(
            source=source.source_type,
            source_location=f"request.{source.source_type}[{source.name!r}]",
            variable=source.name
        )

        traces.append(trace)

    return traces
