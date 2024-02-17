from PIL import Image
from os import listdir
from os.path import isfile, join




original_patterns_folder = "C:\\Users\\braml\\work_documents\\original_patterns"
converted_patterns_folder = "C:\\Users\\braml\\work_documents\\converted_patterns"


def convert_patterns():
    pattern_files = [f for f in listdir(original_patterns_folder) if isfile(join(original_patterns_folder, f))]
    for pattern_file in pattern_files:
        path = join(original_patterns_folder, pattern_file)
        image = Image.open(path)
        image = _to_black_white_image(image)
        path = join(converted_patterns_folder, pattern_file)
        image.save(path)


def _to_black_white_image(image):
    image = image.resize((100, 100))
    if image.mode != '1':
        image = image.convert('1')
    return image

    
