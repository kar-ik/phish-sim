import pytest
from phish_sim.safety_checks import scan_template

def test_scan_template():
    assert len(scan_template("Enter password")) > 0

def test_validate_landing():
    from phish_sim.safety_checks import validate_landing_page
    with pytest.raises(ValueError):
        validate_landing_page('<input type="password">', [])
