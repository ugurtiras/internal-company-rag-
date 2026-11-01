from main import main


def test_main_runs() -> None:
    assert main() == "internal-company-rag is alive"
