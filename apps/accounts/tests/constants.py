from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import BytesIO
from PIL import Image


def create_image(size=(800, 600), image_mode='RGB', image_format='JPEG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return data


# valid data
VALID_FIRST_NAME = 'John'
VALID_LAST_NAME = 'Doe'
VALID_EMAIL = 'john.doe@test.com'
VALID_USERNAME = 'johndoe'
VALID_PASSWORD = 'password123'
VALID_BIRTH_DATE = '1990-01-01'
VALID_GENDER = 'M'
VALID_LOCATION = 'testland'
VALID_PROFILE_PIC = SimpleUploadedFile(
    'profile_pic_test.jpg', create_image().getvalue())

# invalid data
FUTURE_BIRTH_DATE = '2999-01-01'
INVALID_BIRTH_DATE = '12.12.1985'
INVALID_EMAIL = 'invalidemail.com'
TEXT_FILE = SimpleUploadedFile(
            'wrong_file_type.txt', b'This is not an image file.')
