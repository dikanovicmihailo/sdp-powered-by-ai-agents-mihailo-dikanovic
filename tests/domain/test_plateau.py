import pytest

from mars_rover.domain.plateau import Plateau


def test_plateau_is_immutable():
    """PLATEAU-BE-001.1-S1: Domain model enforces immutability"""
    plateau = Plateau(5, 5)
    with pytest.raises(AttributeError):
        plateau.width = 10  # type: ignore[misc]
