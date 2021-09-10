import pytest
import os
import shutil


def del_file(filepath):
    """
    delete files under the path
    :param filepath: file path
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

PATH = lambda path: os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        path
    )
)

if __name__ == '__main__':
    del_file("./tmp")
    # pytest.main(["--alluredir=./tmp/allure_results", "-s", "./tests/ui/"])
