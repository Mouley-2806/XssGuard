
from dataclasses import dataclass, field


@dataclass
class TraceRecord:
    source: str
    source_location: str
    variable: str
    flow_steps: list[str] = field(default_factory=list)
    sink: str | None = None
    sink_location: str | None = None
    context: str = "unknown"

    def add_flow_step(self, step: str) -> None:
        if not isinstance(step, str) or not step.strip():
            raise ValueError("Flow step cannot be empty")
        self.flow_steps.append(step)

