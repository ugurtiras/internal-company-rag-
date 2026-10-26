"""Allow `python -m src.web` to start the web UI."""

from src.web.app import main

if __name__ == "__main__":
    raise SystemExit(main())
