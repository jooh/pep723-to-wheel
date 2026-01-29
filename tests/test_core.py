from pathlib import Path

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
