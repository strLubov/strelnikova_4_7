import pathlib
from zipfile import ZipFile, ZIP_DEFLATED
import os
import pytest
import csv

from PyPDF2 import PdfReader

path = '../examples'
file_dir = os.listdir(path)
directory = pathlib.Path(path)
print(file_dir)


@pytest.fixture()
def create_zip():
    file_info_list_source = []
    with ZipFile("../resources/myzip.zip", "w", compression=ZIP_DEFLATED, compresslevel=5) as myzip:
        for file_path in directory.iterdir():
            myzip.write(file_path, arcname=file_path.name)
            name = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            file_info = f"{name}, {size}"
            file_info_list_source.append(file_info)
    yield file_info_list_source
    os.remove("../resources/myzip.zip")


def test_check_zip(create_zip):
    file_info_list_source = create_zip
    file_info_list = []
    with ZipFile('../resources/myzip.zip', mode='a') as zf:
        for file in zf.infolist():
            name = os.path.basename(file.filename)
            file_info = f"{name}, {file.file_size}"
            file_info_list.append(file_info)
    assert file_info_list_source == file_info_list


def test_check_row_num_in_csv(create_zip):
    row_count_arc = 0
    with open("../examples/example_csv.csv", "r") as f:
        file = csv.reader(f, delimiter=";")
        row_count = sum(1 for row in file)
    with ZipFile('../resources/myzip.zip') as myzip:
        with myzip.open("example_csv.csv", "r") as myfile:
            for line in myfile:
                row_count_arc += 1
    assert row_count == row_count_arc, "Количество строк не совпадает"


def test_check_row_num_in_txt(create_zip):
    with open("../examples/example_txt.txt", "r") as f:
        row_count = sum(1 for row in f)
    with ZipFile('../resources/myzip.zip') as myzip:
        with myzip.open("example_txt.txt", "r") as myfile:
            row_count_arc = sum(1 for row in myfile)
    assert row_count == row_count_arc, "Количество строк не совпадает"


def test_check_page_num_in_pdf(create_zip):
    with open("../examples/example_pdf.pdf", "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        count_page = len(reader.pages)
    with ZipFile('../resources/myzip.zip') as myzip:
        with myzip.open("example_pdf.pdf", "r") as myfile:
            reader = PdfReader(myfile)
            count_page_arc = len(reader.pages)
    assert count_page == count_page_arc, "Количество страниц не совпадает"