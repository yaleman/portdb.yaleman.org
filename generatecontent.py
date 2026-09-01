"""Generate Zola content from the repository's port data."""

from portdb.generator import generate_content


def main() -> None:
    """Generate all tracked port content."""
    print(f"Generated {generate_content()} port pages")


if __name__ == "__main__":
    main()
