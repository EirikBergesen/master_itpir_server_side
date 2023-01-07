from picture_math_module import *


def picture_compare_test():
    # picture_compare function works
    print('Picture compare test: Start')
    assert(picture_compare(Image.open(image_database_list_names_ordered_relativepath[0]), 0))
    print('Picture compare test: Passed')
    
    
def add_picture_function_test():
    # Make empty picture, test add function
    print('Empty picture and picture addition test: Start')
    assert(picture_compare(add_two_images(new_empty_image(), Image.open(image_database_list_names_ordered_relativepath[0])), 0))
    assert(picture_compare(add_two_images(Image.open(image_database_list_names_ordered_relativepath[0]), new_empty_image()), 0))
    print('Empty picture and picture addition test: Passed')
        

def subtract_picture_test():
    # Test subtract function, assert empty picture
    print('Subtract and assert empty: Start')
    assert(all_pixels_in_images_compare(subtract_two_images(Image.open(image_database_list_names_ordered_relativepath[3]),
                                                               Image.open(image_database_list_names_ordered_relativepath[3])), new_empty_image()))
    assert(all_pixels_in_images_compare(subtract_two_images(Image.open(image_database_list_names_ordered_relativepath[3]),
                                                               Image.open(image_database_list_names_ordered_relativepath[3])), new_empty_image()))
    print('Subtract and assert empty: Passed')
    
    
def add_and_subtract_test():
    # Add then subtract
    print('Add, then Subtract and assert empty: Start')
    added_pic_0 = add_two_images(Image.open(image_database_list_names_ordered_relativepath[6]), new_empty_image())
    added_pic_1 = add_two_images(Image.open(image_database_list_names_ordered_relativepath[6]), new_empty_image())
    subtracted_pic_0 = subtract_two_images(added_pic_0, Image.open(image_database_list_names_ordered_relativepath[6]))
    subtracted_pic_1 = subtract_two_images(Image.open(image_database_list_names_ordered_relativepath[6]), added_pic_1)
    assert(all_pixels_in_images_compare(subtracted_pic_0, new_empty_image()))
    assert(all_pixels_in_images_compare(subtracted_pic_1, new_empty_image()))
    print('Add, then Subtract and assert empty: Passed')


def more_adding_and_subtracting_test():
    # Several adds and subs
    print('Several Adds and subtracts: Start')
    s_add_0 = add_two_images(Image.open(image_database_list_names_ordered_relativepath[6]), Image.open(image_database_list_names_ordered_relativepath[7]))
    # 7 and 6
    s_sub_0 = subtract_two_images(s_add_0, Image.open(image_database_list_names_ordered_relativepath[5]))
    # 7, 6 and -5
    s_sub_1 = subtract_two_images(s_sub_0, Image.open(image_database_list_names_ordered_relativepath[7]))
    # 6 and -5
    s_sub_2 = subtract_two_images(s_sub_1, Image.open(image_database_list_names_ordered_relativepath[6]))
    # -5
    s_add_1 = add_two_images(s_sub_2, Image.open(image_database_list_names_ordered_relativepath[7]))
    # -5 and 7
    s_add_2 = add_two_images(s_add_1, Image.open(image_database_list_names_ordered_relativepath[5]))
    # 7
    assert(picture_compare(s_add_2, 7))
    print('Several Adds and subtracts: Passed')


def adding_images_in_list_test():
    print('Adding images in list test: Start')
    add_list_image = add_several_images(load_several_images_from_path([image_database_list_names_ordered_relativepath[0],
                                                     image_database_list_names_ordered_relativepath[1],
                                                     image_database_list_names_ordered_relativepath[4],
                                                     image_database_list_names_ordered_relativepath[5]]))
    compound_pic = new_empty_image()
    s_add_0 = add_two_images(compound_pic, Image.open(image_database_list_names_ordered_relativepath[0]))
    s_add_1 = add_two_images(s_add_0, Image.open(image_database_list_names_ordered_relativepath[1]))
    s_add_2 = add_two_images(s_add_1, Image.open(image_database_list_names_ordered_relativepath[4]))
    s_add_3 = add_two_images(s_add_2, Image.open(image_database_list_names_ordered_relativepath[5]))
    assert(all_pixels_in_images_compare(s_add_3, add_list_image))
    print('Adding images in list test: Passed')
    
    
def subtracting_images_in_list_test():
    print('Subtracting images in list test: Start')
    sub_list_image = subtract_several_images(load_several_images_from_path([image_database_list_names_ordered_relativepath[0],
                                                     image_database_list_names_ordered_relativepath[7],
                                                     image_database_list_names_ordered_relativepath[4],
                                                     image_database_list_names_ordered_relativepath[5]]))
    compound_pic = new_empty_image()
    s_sub_0 = subtract_two_images(compound_pic, Image.open(image_database_list_names_ordered_relativepath[0]))
    s_sub_1 = subtract_two_images(s_sub_0, Image.open(image_database_list_names_ordered_relativepath[7]))
    s_sub_2 = subtract_two_images(s_sub_1, Image.open(image_database_list_names_ordered_relativepath[4]))
    s_sub_3 = subtract_two_images(s_sub_2, Image.open(image_database_list_names_ordered_relativepath[5]))
    assert(all_pixels_in_images_compare(s_sub_3, sub_list_image))
    print('Subtracting images in list test: Passed')


def run_picture_math_module_test():
    picture_compare_test()
    add_picture_function_test()
    subtract_picture_test()
    add_and_subtract_test()
    more_adding_and_subtracting_test()
    adding_images_in_list_test()
    subtracting_images_in_list_test()


if __name__ == "__main__":
    run_picture_math_module_test()
    """
    path_img_00 = 'picture_math_folder.py/tree-picture_320240_00.png'
    path_img_01 = 'picture_math_folder.py/tree-picture_320240_01.png'

    print(img_00.format, img_00.size, img_00.mode)

    img = add_two_images(img_00, img_01)

    img.save('two_added_images.png', optimize=False, compress_level=0, bits=(256*3))
    img.show()

    """