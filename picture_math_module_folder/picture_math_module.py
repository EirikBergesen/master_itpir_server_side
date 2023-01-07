import numpy as np
from PIL import Image


image_database_list_names_ordered_relativepath = [
    'tree-picture_320240_00.png',
    'tree-picture_320240_01.png',
    'tree-picture_320240_02.png',
    'tree-picture_320240_03.png',
    'tree-picture_320240_04.png',
    'tree-picture_320240_05.png',
    'tree-picture_320240_06.png',
    'tree-picture_320240_07.png',
    'tree-picture_320240_08.png',
    'tree-picture_320240_09.png'
]


def subtract_two_pixels(pixel_0:tuple, pixel_1:tuple):
    red = (pixel_0[0] - pixel_1[0]) % 256
    green = (pixel_0[1] - pixel_1[1]) % 256
    blue = (pixel_0[2] - pixel_1[2]) % 256
    return tuple((red, green, blue))


def add_two_pixels(pixel_0:tuple, pixel_1:tuple):
    red = (pixel_0[0] + pixel_1[0]) % 256
    green = (pixel_0[1] + pixel_1[1]) % 256
    blue = (pixel_0[2] + pixel_1[2]) % 256
    return tuple((red, green, blue))


def add_two_images(image_0:Image, image_1:Image):
    '''Add two images. These needs to be of the same size.'''
    if not image_0.size == image_1.size:
        return False
    
    image_0_pixels = image_0.load()
    image_1_pixels = image_1.load()
    new_image_pixels = image_0_pixels
    
    (image_size_x, image_size_y) = image_0.size
    for col in range(image_size_y):
        for row in range(image_size_x):
            
            new_pixel_tuple = add_two_pixels(image_0_pixels[row, col], image_1_pixels[row, col])
            new_image_pixels[row, col] = (new_pixel_tuple)

    img = Image.new(size=(320, 240), mode="RGB")
    for row in range(320):
        for col in range(240):
            img.putpixel((row, col), tuple(new_image_pixels[row, col]))
    return img
            
            
def subtract_two_images(image_0:Image, image_1:Image):
    '''Subtract two images. These needs to be of the same size.'''
    if not image_0.size == image_1.size:
        return False
    
    image_0_pixels = image_0.load()
    image_1_pixels = image_1.load()
    new_image_pixels = image_0_pixels
    
    (image_size_x, image_size_y) = image_0.size
    for col in range(image_size_y):
        for row in range(image_size_x):
            
            new_pixel_tuple = subtract_two_pixels(image_0_pixels[row, col], image_1_pixels[row, col])
            new_image_pixels[row, col] = (new_pixel_tuple)

    img = Image.new(size=(320, 240), mode="RGB")
    for row in range(320):
        for col in range(240):
            img.putpixel((row, col), tuple(new_image_pixels[row, col]))
    return img


def new_empty_image(pic_size:tuple = (320, 240)):
    """Returns a new empty image of type Image

    Args:
        pic_size (tuple, optional): Width and height. Defaults to (320, 240).

    Returns:
        Image: Empty picture
    """
    img = Image.new(size=pic_size, mode="RGB")
    for row in range(pic_size[0]):
        for col in range(pic_size[1]):
            img.putpixel((row, col), tuple((0, 0, 0)))
    return img
    

def all_pixels_in_images_compare(image_0:Image, image_1:Image):
    '''Comparing two images, if they are the same. As in: all pixels have the same values.'''
    if not image_0.size == image_1.size:
        return False
    image_0_pixels = image_0.load()
    image_1_pixels = image_1.load()
    
    (image_size_x, image_size_y) = image_0.size
    for col in range(image_size_y):
        for row in range(image_size_x):
            
            if not image_0_pixels[row, col] == image_1_pixels[row, col]:
                return False

    return True


def add_several_images(image_list:list):
    new_image = new_empty_image()
    for image in image_list:
        new_image = add_two_images(new_image, image)
    return new_image


def subtract_several_images(image_list:list):
    new_image = new_empty_image()
    for image in image_list:
        new_image = subtract_two_images(new_image, image)
    return new_image
    
    
def picture_compare(img_00:Image, picture_number_in_database:int):
    image_1 = image_database_list_names_ordered_relativepath[picture_number_in_database]
    img_01 = Image.open(image_1)
    return all_pixels_in_images_compare(img_00, img_01)

    
def image_is_in_picture_list(img:Image):
    for i in range(len(image_database_list_names_ordered_relativepath)):
        if picture_compare(img, i):
            return True
    return False


def load_image_from_path(path:str):
    return Image.open(path)


def load_several_images_from_path(path_list:list):
    image_list = []
    for picture in path_list:
        image_list.append(load_image_from_path(picture))
    return image_list


def save_image_as(img:Image, path:str):
    """Stores an image as compression less png

    Args:
        img (Image): Image to be saved/stored to file
        path (str): Path for that file to be stored to
    """    
    img.save(path, bitmap_format='png', optimize=False,compress_level=0, bits=(256*3))
