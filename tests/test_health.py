def test_import():
    """Basic smoke test - check if app module can be imported"""
    try:
        from app.main import app
        assert app is not None
    except ImportError:
        assert False, "Failed to import app"

def test_basic():
    """Basic sanity check"""
    assert True
