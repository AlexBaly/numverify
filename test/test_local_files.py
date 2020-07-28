import os
import shutil

import pytest

from numverify.sorter.local_files.local_files import LocalFiles
from test.constants import BASE_DIR, IN_DIR, OUT_DIR


def test_init():
    try:
        LocalFiles("RU","USA")
        assert False, "ValueError for incorrect paths"
    except ValueError:
        assert True

@pytest.fixture(autouse=True)
def file_str():
    os.makedirs(IN_DIR)
    os.makedirs(OUT_DIR)
    for file in os.listdir(r"test\resources"):
        shutil.copy(os.path.join(r"test\resources", file), os.path.join(IN_DIR, file))
    yield
    shutil.rmtree(BASE_DIR)

def test_read_file():
    lf = LocalFiles(IN_DIR, OUT_DIR)
    for file in os.listdir(IN_DIR):
        assert  len(lf.read_file(os.path.join(IN_DIR, file))) < 400, "Max len number"

def test_make_out_dir():
    lf = LocalFiles(IN_DIR, OUT_DIR)
    lf._make_out_dir("UK")
    assert os.path.isdir(os.path.join(OUT_DIR,"UK")), "incorrect"
    lf._make_out_dir("UK")
    assert os.path.isdir(os.path.join(OUT_DIR, "UK")), "incorrect"
    try:
        lf._make_out_dir('')
        assert  False, "no ValueErroor for empty"
    except ValueError:
        assert True

def test_prepare_paths():
    lf = LocalFiles(IN_DIR,OUT_DIR)
    lf.prepare_paths()
    assert len(lf.api.phone) == len(os.listdir(IN_DIR)), "incorrect len"

def test_phone():
    lf = LocalFiles(IN_DIR,OUT_DIR)
    lf.move_phone()
    print(len(os.listdir(OUT_DIR)))
    assert  len(os.listdir(OUT_DIR)) == 1, "some file appeared"
    lf.prepare_paths()
    lf.move_phone()
    assert len(os.listdir(OUT_DIR)) > 0 , "no directory create"
    for dir in os.listdir(OUT_DIR):
         assert os.path.isdir(os.path.join(OUT_DIR,dir)), "not a directory"
    for dir in os.listdir(OUT_DIR):
         for file in os.listdir(os.path.join(OUT_DIR, dir)):
             assert  os.path.isfile(os.path.join(OUT_DIR,dir,file)), "not a directory files"