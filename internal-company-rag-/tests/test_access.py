from src.ingestion.access import is_valid_access_label


def test_known_labels_are_valid() -> None:
    assert is_valid_access_label("tum_calisanlar")
    assert is_valid_access_label("ik_gizli")


def test_unknown_label_is_invalid() -> None:
    assert not is_valid_access_label("herkes")


def test_empty_or_missing_label_is_invalid() -> None:
    assert not is_valid_access_label(None)
    assert not is_valid_access_label("")
