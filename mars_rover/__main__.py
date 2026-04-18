"""Minimal CLI entrypoint for the Mars Rover package."""

from mars_rover import turn_left


def main() -> None:
    """Run a tiny smoke output so container runtime is executable."""
    print("Mars Rover CLI ready")
    print(f"turn_left(N) -> {turn_left('N')}")


if __name__ == "__main__":
    main()
