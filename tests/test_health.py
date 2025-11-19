import pytest

def test_basic_sanity():
    """Basic sanity check"""
    assert 1 + 1 == 2
    assert True is True

def test_fastapi_import():
    """Test that FastAPI can be imported"""
    try:
        import fastapi
        assert fastapi.__version__ is not None
    except ImportError:
        pytest.fail("Failed to import FastAPI")

def test_sqlalchemy_import():
    """Test that SQLAlchemy can be imported"""
    try:
        import sqlalchemy
        assert sqlalchemy.__version__ is not None
    except ImportError:
        pytest.fail("Failed to import SQLAlchemy")
