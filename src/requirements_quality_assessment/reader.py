"""Read one UTF-8 source line per requirement."""

from pathlib import Path

from .domain.core import Requirement


class RequirementReader:
    """Convert non-empty physical lines into source-ordered requirements."""

    def read(self, path: str | Path) -> tuple[Requirement, ...]:
        requirements: list[Requirement] = []
        with Path(path).open("r", encoding="utf-8") as source:
            for source_line, line in enumerate(source, start=1):
                text = line.strip()
                if text:
                    requirements.append(
                        Requirement(f"R{len(requirements) + 1:03d}", source_line, text)
                    )
        return tuple(requirements)
