# Для считывания PDF
import pypdf
# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# Для извлечения текста из таблиц в PDF
import pdfplumber
# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path
# Для выполнения OCR, чтобы извлекать тексты из изображений 
import pytesseract 
# Для удаления дополнительно созданных файлов
import os


pdf_path = 'menu_example.pdf'

# enumerate(extract_pages(pdf_path))

# for pagenum, page in enumerate(extract_pages(pdf_path)):
#     print(pagenum, page, sep=" | ")
