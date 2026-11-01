"""Tests that the committed config.yaml roles reference known labels only."""

from pathlib import Path

from src.ingestion.access import ALLOWED_ACCESS_LABELS
from src.utils.config import load_config

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"


def test_every_role_uses_known_labels_and_includes_tum_calisanlar() -> None:
    cfg = load_config(CONFIG_PATH)
    for role, labels in cfg["roles"].items():
        assert set(labels) <= ALLOWED_ACCESS_LABELS, f"role {role} has unknown labels"
        assert "tum_calisanlar" in labels, f"role {role} cannot read tum_calisanlar"


def test_management_reads_all_nine_labels() -> None:
    cfg = load_config(CONFIG_PATH)
    assert set(cfg["roles"]["yonetim"]) == ALLOWED_ACCESS_LABELS
    assert len(ALLOWED_ACCESS_LABELS) == 9
