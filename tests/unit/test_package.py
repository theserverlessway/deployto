import pytest
from path import Path
import os
from deployto import package
from io import BytesIO
import zipfile
from uuid import uuid4


def uuids():
    return sorted([str(uuid4()) for _ in range(2)])


@pytest.fixture
def folder():
    return str(uuid4())


@pytest.fixture
def folder_files():
    return uuids()


@pytest.fixture
def top_files():
    return uuids()


@pytest.fixture()
def testfolder(tmpdir, folder, folder_files, top_files):
    with Path(tmpdir):
        os.makedirs(folder)
        for file in folder_files:
            with open('{}/{}'.format(folder, file), 'w') as f:
                f.write(file)
        for file in top_files:
            with open('{}'.format(file), 'w') as f:
                f.write(file)
    return tmpdir


def namelist(file):
    return zipfile.ZipFile(BytesIO(file)).namelist()


def content(file, path):
    with zipfile.ZipFile(BytesIO(file)).open(path) as f:
        return f.read().decode()


def test_includes_content_of_files(testfolder, top_files):
    with Path(testfolder):
        result = package.package(top_files[:1])
        assert top_files[:1] == namelist(result)
        assert top_files[0] == content(result, top_files[0])


def test_packaging_folder_to_root(testfolder, folder, folder_files):
    with Path(testfolder):
        result = package.package(['{}:'.format(folder)])
        assert folder_files == sorted(namelist(result))


def test_package_single_file(testfolder, top_files):
    with Path(testfolder):
        result = package.package(['{}'.format(top_files[0])])
        assert [top_files[0]] == namelist(result)


def test_package_single_file_and_move(testfolder, folder, folder_files):
    with Path(testfolder):
        result = package.package(['{}/{}:'.format(folder, folder_files[0])])
        assert folder_files[:1] == namelist(result)


def test_empty_paths(testfolder, folder, folder_files, top_files):
    with Path(testfolder):
        result = package.package([])
        assert [] == namelist(result)


def test_package_whole_folder(testfolder, folder, folder_files, top_files):
    with Path(testfolder):
        result = package.package(['.'])
        assert sorted(top_files + [folder + '/' + file for file in folder_files]) == sorted(namelist(result))


def test_package_folder_into_other_folder(testfolder, folder, folder_files):
    target = str(uuid4())
    with Path(testfolder):
        result = package.package(['{}:{}'.format(folder, target)])
        assert sorted([target + '/' + file for file in folder_files]) == sorted(namelist(result))


def test_include_multiple_paths(testfolder, top_files):
    with Path(testfolder):
        result = package.package(top_files)
        assert sorted(top_files) == sorted(namelist(result))


def test_include_and_rename_file(testfolder, top_files):
    target = str(uuid4())
    with Path(testfolder):
        result = package.package(['{}:{}'.format(top_files[0], target)])
        assert [target] == namelist(result)
        assert top_files[0] == content(result, target)


def test_raises_exception_if_it_cant_find_paths(testfolder):
    target = str(uuid4())
    with Path(testfolder):
        with pytest.raises(package.PackagingException):
            package.package([target])
