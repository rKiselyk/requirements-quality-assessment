"""Tests for the approved UTF-8, one-physical-line input contract."""

from pathlib import Path

import pytest

from requirements_quality_assessment.domain.core import Requirement
from requirements_quality_assessment.reader import RequirementReader


@pytest.mark.parametrize("as_string", [False, True])
def test_reads_requirements_in_order_with_physical_source_lines(
    tmp_path: Path, as_string: bool
) -> None:
    path = tmp_path / "requirements.txt"
    path.write_text(
        "System shall authenticate the user.\n"
        "\n"
        "System shall quickly load data.\n"
        "Password shall contain at least 12 characters.\n",
        encoding="utf-8",
    )

    result = RequirementReader().read(str(path) if as_string else path)

    assert result == (
        Requirement("R001", 1, "System shall authenticate the user."),
        Requirement("R002", 3, "System shall quickly load data."),
        Requirement("R003", 4, "Password shall contain at least 12 characters."),
    )


def test_ukrainian_text_round_trips_without_rewriting(tmp_path: Path) -> None:
    path = tmp_path / "ukrainian.txt"
    first = "Система повинна сформувати звіт."
    second = "Маршрут доставки повинен швидко перераховуватися."
    path.write_text(f"{first}\n{second}\n", encoding="utf-8")

    assert RequirementReader().read(path) == (
        Requirement("R001", 1, first),
        Requirement("R002", 2, second),
    )


def test_trims_only_outer_whitespace_and_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "requirements.txt"
    path.write_text(
        "\n   \n\t\t\n   Система формує звіт.   \n"
        "\tДоступність має бути не нижче 99,9 %;  час відгуку ≤ 2 с.\t\n"
        "  Об'єкт-1:  100 % ≤ 200; зв'язок збережено.  \n",
        encoding="utf-8",
    )

    assert RequirementReader().read(path) == (
        Requirement("R001", 4, "Система формує звіт."),
        Requirement("R002", 5, "Доступність має бути не нижче 99,9 %;  час відгуку ≤ 2 с."),
        Requirement("R003", 6, "Об'єкт-1:  100 % ≤ 200; зв'язок збережено."),
    )


def test_multiple_sentences_stay_on_one_requirement(tmp_path: Path) -> None:
    path = tmp_path / "requirements.txt"
    text = "Система зберігає запит. Після цього система надсилає повідомлення."
    path.write_text(text + "\n", encoding="utf-8")

    assert RequirementReader().read(path) == (Requirement("R001", 1, text),)


@pytest.mark.parametrize("content", ["", "\n   \n\t\n"])
def test_empty_or_all_blank_file_returns_empty_tuple(tmp_path: Path, content: str) -> None:
    path = tmp_path / "requirements.txt"
    path.write_text(content, encoding="utf-8")

    assert RequirementReader().read(path) == ()


def test_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        RequirementReader().read(tmp_path / "missing.txt")


def test_directory_is_not_treated_as_empty_input(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        RequirementReader().read(tmp_path)


def test_invalid_utf8_raises_decode_error(tmp_path: Path) -> None:
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"Valid line\n\xff\n")

    with pytest.raises(UnicodeDecodeError):
        RequirementReader().read(path)


def test_id_format_continues_after_three_digits(tmp_path: Path) -> None:
    path = tmp_path / "requirements.txt"
    path.write_text("Line\n" * 1000, encoding="utf-8")

    result = RequirementReader().read(path)

    assert len(result) == 1000
    assert result[-1] == Requirement("R1000", 1000, "Line")
