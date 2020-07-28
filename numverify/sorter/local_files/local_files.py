import os
import shutil

from numverify.sorter.api.api import API
from numverify.sorter.api.constants import NOT_COUNTRY


class LocalFiles:
    def __init__(self, in_dir, out_dir):
        if not os.path.isdir(in_dir) or not os.path.isdir(out_dir):
                raise ValueError("Paths must be directories")
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.api = API()

    def read_file(self, file):
        with open(os.path.join(self.in_dir, file), encoding="utf-8") as f:
            text = f.read(20)
        return text

    def _make_out_dir(self, phone):
        if phone == '':
            raise ValueError("directory name empty")
        full_path = os.path.join(self.out_dir, phone)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    def prepare_paths(self):
        texts = []
        for file in os.listdir(self.in_dir):
            texts.append(self.read_file(file))
        self.api.search_country(texts)

    def move_phone(self):
        for file in os.listdir(self.in_dir):
            text = self.read_file(file)
            phone = self.api.get_country(text)
            if phone is None: phone = NOT_COUNTRY
            if phone is False: phone = NOT_COUNTRY
            self._make_out_dir(phone)
            shutil.copy(
                 os.path.join(self.in_dir, file),
                 os.path.join(self.out_dir, phone, file)
            )