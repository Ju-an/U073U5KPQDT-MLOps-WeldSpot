import os
import shutil

import pytest

from service.cloud_storage import download_roboflow


def test_download_roboflow():
    tmp_dir = "temp"
    os.makedirs(tmp_dir, exist_ok=True)


    # Execute the function
    total = download_roboflow(f"modeling/{tmp_dir}")

    # Verify that files were downloaded
    assert total > 0, "No files were downloaded"
