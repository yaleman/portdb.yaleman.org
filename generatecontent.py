"""Generate Zola content from the repository's port data."""

from pathlib import Path

DATA_DIR = Path("data")
CONTENT_DIR = Path("content")
PROTOCOLS = ("tcp", "udp")


def render_port(protocol: str, port: int, notes: str | None, iana_data: str | None) -> str:
    """Render one port page with Zola front matter."""
    sections = [
        "+++",
        f'title = "{port}"',
        f"weight = {port}",
        'template = "port.html"',
        f'path = "{protocol}/{port}"',
        "[extra]",
        f'protocol = "{protocol}"',
        "+++",
    ]
    if notes:
        sections.extend(("", notes.strip()))
    if iana_data:
        sections.extend(("", "## IANA Data", "", iana_data.strip()))
    return "\n".join(sections) + "\n"


def render_section(protocol: str) -> str:
    """Render a paginated protocol index."""
    return f'''+++
title = "{protocol.upper()} ports"
description = "Browse known {protocol.upper()} port numbers."
sort_by = "weight"
paginate_by = 100
template = "section.html"
page_template = "port.html"
aliases = ["/category/{protocol}.html"]
+++
'''


def generate_protocol(protocol: str) -> int:
    """Generate every page for one protocol and return the page count."""
    source_dir = DATA_DIR / protocol
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Missing protocol data directory: {source_dir}")

    destination_dir = CONTENT_DIR / protocol
    destination_dir.mkdir(parents=True, exist_ok=True)
    (destination_dir / "_index.md").write_text(render_section(protocol), encoding="utf-8")

    generated = 0
    port_directories = (path for path in source_dir.iterdir() if path.is_dir() and path.name.isdigit())
    for port_dir in sorted(port_directories, key=lambda path: int(path.name)):
        notes_path = port_dir / "notes.md"
        iana_path = port_dir / "iana.md"
        notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else None
        iana_data = iana_path.read_text(encoding="utf-8") if iana_path.exists() else None
        if notes is None and iana_data is None:
            raise ValueError(f"No notes or IANA data found for {protocol}/{port_dir.name}")

        page = render_port(protocol, int(port_dir.name), notes, iana_data)
        (destination_dir / f"{port_dir.name}.md").write_text(page, encoding="utf-8")
        generated += 1
    return generated


def main() -> None:
    """Generate all tracked port content."""
    total = sum(generate_protocol(protocol) for protocol in PROTOCOLS)
    print(f"Generated {total} port pages")


if __name__ == "__main__":
    main()
