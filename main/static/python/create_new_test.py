from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent


MEDIA_DIR = os.path.join(BASE_DIR,'media')
TEST_DIR = os.path.join(MEDIA_DIR, 'tests')


def create_new_test(name):
    try:
        new_test_dir = os.path.join(TEST_DIR, name)
        os.mkdir(new_test_dir)
        folders_to_create = ['input', 'sample_output']

        for folder in folders_to_create:
            new_folder_dir = os.path.join(new_test_dir, folder)
            os.mkdir(new_folder_dir)
    except:
        print('Cant Create New Test')

create_new_test('test1')