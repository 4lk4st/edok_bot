from PIL import Image
from pdf2image import convert_from_path

import pytesseract
import re
import os


temp_files = [
   'menu_image.png',
   'output.txt'
]

for temp_file in temp_files:
    if os.path.isfile(os.path.join(os.path.dirname(__file__), temp_file)):
        os.remove(os.path.join(os.path.dirname(__file__), temp_file))


pytesseract.pytesseract.tesseract_cmd = r'D:\Программы\Tesseract\tesseract'
poppler_path = r"D:\Программы\Tesseract\poppler-24.02.0\Library\bin"
pdf_path = 'menu_example.pdf'

pages = convert_from_path(pdf_path, 500, poppler_path=poppler_path)
for page in pages:
    page.save('menu_image.png', 'PNG')


output_text = pytesseract.image_to_string(Image.open('menu_image.png'), lang='rus')

# text_without_brackets = re.compile(r'\([^()]*\)').sub('', output_text)
# text_without_gr = re.compile(r'\b\d{3}гр\b').sub('', text_without_brackets)

regex_rules = [
    r'\([^()]*\)',
    r'\b\d{3}гр\b',
    r'\b\d{3}\sгр\b',
    r'\b\d{3}г\b',
    r'\b\d{2}\b',
]

clean_text = ''

for rule in regex_rules:
    clean_text = re.compile(rule).sub('', output_text)
    output_text = clean_text

with open("output.txt", "w", encoding='utf-8') as f:
    f.write(output_text)
