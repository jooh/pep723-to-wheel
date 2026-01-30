from __future__ import annotations

import os
import pathlib
import re
import tomllib
from dataclasses import dataclass


VERSION_PATTERN = re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "Version | None":
        match = VERSION_PATTERN.match(value)
        if not match:
            return None
        return cls(
            major=int(match.group("major")),
            minor=int(match.group("minor")),
            patch=int(match.group("patch")),
        )

    def bump_patch(self) -> "Version":
        return Version(self.major, self.minor, self.patch + 1)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def read_current_version(pyproject_path: pathlib.Path) -> Version:
    data = tomllib.loads(pyproject_path.read_text())
    current = data["project"]["version"]
    parsed = Version.parse(current)
    if not parsed:
        raise ValueError(f"Invalid project.version in {pyproject_path}: {current}")
    return parsed


def write_version(pyproject_path: pathlib.Path, version: Version) -> None:
    content = pyproject_path.read_text()
    updated = re.sub(
        r'(?m)^version = "[^"]+"',
        f'version = "{version}"',
        content,
        count=1,
    )
    if updated == content:
        raise ValueError(f"Failed to update version in {pyproject_path}")
    pyproject_path.write_text(updated)


def resolve_version(current: Version, latest_tag: str | None) -> Version:
    if not latest_tag:
        return current
    parsed = Version.parse(latest_tag.lstrip("v"))
    if not parsed:
        return current
    if current.major == parsed.major and current.minor == parsed.minor:
        return current.bump_patch()
    return current


def main() -> None:
    pyproject_path = pathlib.Path("pyproject.toml")
    current = read_current_version(pyproject_path)
    new_version = resolve_version(current, os.environ.get("LATEST_TAG"))

    if new_version != current:
        write_version(pyproject_path, new_version)

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with pathlib.Path(output_path).open("a") as handle:
            handle.write(f"version={new_version}\n")
    else:
        raise RuntimeError("GITHUB_OUTPUT is not set")
    print(f"Resolved version: {new_version}")


if __name__ == "__main__":
    main()
