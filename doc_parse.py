import typing
import re
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract

"""
Формат файлов: PDF(Сканы Jpeg), JPEG
Шаблоны данных: Различные N
Искомое поле: Заводской серийный номер
Формат номера: En, Буквы, Цифры, Тире
"""

# TODO: PDF image extract
# TODO: Image to text
# TODO: Serial Number Extract

"""
DB: Путь к файлу,
- Ошибки
- Распознанные номера
- Не распознано
"""


def pdf_image_extract(pdf_path: Path, image_path: Path) -> typing.List[Path]:
    result = []
    with pdf_path.open("rb") as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError as exc:
            print(exc)
            return result

        for page_num, page in enumerate(pdf_file.pages, 1):
            img_data = page["/Resources"]["/XObject"]["/Im0"]._data
            img_file_name = f"{pdf_path.name}_{page_num}"
            img_path = image_path.joinpath(img_file_name)
            img_path.write_bytes(img_data)
            result.append(img_path)

    return result


def get_serial_number(img_path: Path) -> typing.List[str]:
    result = []
    image = Image.open(img_path)
    text_rus = pytesseract.image_to_string(image, "rus")
    pattern = re.compile(r"(заводской.*[номер|№])")
    matchs = len(re.findall(pattern, text_rus))
    if matchs:
        text_eng = pytesseract.image_to_string(image, "eng").split("\n")
        for idx, line in enumerate(text_rus.split("\n")):
            if re.match(pattern, line):
                result.append(text_eng[idx].split()[-1])
                if len(result) == matchs:
                    break
    return result


if __name__ == "__main__":
    IMAGES_PATH = Path(__file__).parent.joinpath("images")
    if not IMAGES_PATH.exists():
        IMAGES_PATH.mkdir()
    pdf_path_temp = Path(__file__).parent.joinpath("8416_4.pdf")
    images = pdf_image_extract(pdf_path_temp, IMAGES_PATH)
    numbers = list(map(get_serial_number, images))
    print(1)
