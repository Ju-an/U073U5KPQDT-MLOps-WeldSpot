import pytest, shutil, os

from service.cloud_storage import download_roboflow

def test_download_roboflow():
    tmp_dir = "tmp"
    os.mkdir(tmp_dir)
    
    try:
        # Execute the function
        download_roboflow(tmp_dir)
        
        # Verify that files are downloaded
        assert len(os.listdir(tmp_dir)) > 0, "No files were downloaded"
        
    finally:
        # Teardown
        shutil.rmtree(tmp_dir)