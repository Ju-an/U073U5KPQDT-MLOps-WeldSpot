import pytest

from service.cloud_storage import init_firebase_storage


def test_init_firebase_storage():
    storage = init_firebase_storage()
    assert storage is not None
