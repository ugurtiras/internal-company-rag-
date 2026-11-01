"""Role-based access decisions. The single place where access is decided."""

from src.ingestion.access import ALLOWED_ACCESS_LABELS


class UnknownRoleError(ValueError):
    """Raised when a role is not defined in the configuration."""


def allowed_labels(role: str, roles_cfg: dict) -> frozenset[str]:
    """Return the set of access labels the role may read.

    Raises UnknownRoleError for a role missing from the config; unknown
    roles never receive access. Raises ValueError if the role lists a
    label outside ALLOWED_ACCESS_LABELS.
    """
    if role not in roles_cfg:
        raise UnknownRoleError(f"unknown role: {role!r}")
    labels = roles_cfg[role]
    invalid = sorted(set(labels) - ALLOWED_ACCESS_LABELS)
    if invalid:
        raise ValueError(f"role {role!r} lists invalid access labels: {invalid}")
    return frozenset(labels)
