"""Access labels that a document is allowed to carry."""

ALLOWED_ACCESS_LABELS = frozenset(
    {
        "tum_calisanlar",
        "muhendislik",
        "destek",
        "satis",
        "finans",
        "hukuk",
        "yonetim",
        "ik_gizli",
        "ik",
    }
)


def is_valid_access_label(label: object) -> bool:
    """Return True only if label is one of the 9 known access labels."""
    return isinstance(label, str) and label in ALLOWED_ACCESS_LABELS
