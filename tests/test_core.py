from pathlib import Path
from datetime import datetime
import os

from pep723_to_wheel import core


def test_build_and_import_round_trip(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "# /// script",
                '# requires-python = ">=3.12"',
                '# dependencies = ["requests>=2.0"]',
                "# ///",
                "print('hello')",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = core.build_script_to_wheel(script, tmp_path)

    assert result.wheel_path.name.endswith(".whl")
    assert result.wheel_path.exists()

    output_path = tmp_path / "reconstructed.py"
    import_result = core.import_wheel_to_script(str(result.wheel_path), output_path)

    assert import_result.script_path == output_path
    assert import_result.script_path.read_text(encoding="utf-8") == script.read_text(
        encoding="utf-8"
    )


def test_pep723_header_parsing_and_render(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "# /// script",
                '# requires-python = ">=3.12"',
                '# dependencies = ["pydantic>=2.5", "httpx"]',
                "# ///",
                "print('hello')",
                "",
            ]
        ),
        encoding="utf-8",
    )

    header = core.Pep723Header.from_script(script)

    assert header.requires_python == ">=3.12"
    assert header.dependencies == ["pydantic>=2.5", "httpx"]
    assert header.render_block() == "\n".join(
        [
            "# /// script",
            '# requires-python = ">=3.12"',
            '# dependencies = ["pydantic>=2.5", "httpx"]',
            "# ///",
        ]
    )


def test_pep723_header_allows_missing_requires_python(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "# /// script",
                '# dependencies = ["pydantic>=2.5"]',
                "# ///",
                "print('hello')",
                "",
            ]
        ),
        encoding="utf-8",
    )

    header = core.Pep723Header.from_script(script)

    assert header.requires_python is None
    assert header.dependencies == ["pydantic>=2.5"]
    assert header.render_block() == "\n".join(
        [
            "# /// script",
            '# dependencies = ["pydantic>=2.5"]',
            "# ///",
        ]
    )


def test_build_uses_specified_version(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "# /// script",
                '# requires-python = ">=3.12"',
                "# ///",
                "print('hello')",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = core.build_script_to_wheel(script, tmp_path, version="2024.12.25")

    assert "2024.12.25" in result.wheel_path.name


def test_build_defaults_to_mtime_calver(tmp_path: Path) -> None:
    script = tmp_path / "script.py"
    script.write_text(
        "\n".join(
            [
                "# /// script",
                '# requires-python = ">=3.12"',
                "# ///",
                "print('hello')",
                "",
            ]
        ),
        encoding="utf-8",
    )
    fixed_timestamp = datetime(2024, 12, 25, 12, 34, 56, tzinfo=core.UTC).timestamp()
    os.utime(script, (fixed_timestamp, fixed_timestamp))

    result = core.build_script_to_wheel(script, tmp_path)

    assert "2024.12.25" in result.wheel_path.name
    assert str(int(fixed_timestamp)) in result.wheel_path.name
