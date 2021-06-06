from PIL import Image, ImageEnhance
from simpleimage import SimpleImage

# Cinemize! by James Kwon Lee (5.25.2021)
# This simple app uses Python3 to take any image and bump up the contrast + add corresponding black bars to make your average photos more cinematic.
# We've included four of the most popular aspect ratios you can choose from to edit your photos!

# Aspect Ratio References
ASPECT_RATIO = {"VistaVision": 1.85, "CinemaScope": 2.35, "European WideScreen": 1.66, "Academy": 1.37}
ASPECT_RATIO_KEY = {1: "VistaVision", 2: "CinemaScope", 3: "European WideScreen", 4: "Academy"}

# corresponding key values
VALID_INPUTS = [1, 2, 3, 4]

# Original Image file
IMAGE = "Stanford_Campus.jpg"

CONTRAST_FACTOR = 1.45

def main():
    """
    # This is slow! Only works if image is small.
    original_image = SimpleImage(IMAGE)
    original_image.show()
    """
    print("Welcome to Cinemize!")
    valid_input = False

    while valid_input is False:
        print("Please select an aspect ratio for your image by typing in the corresponding number from our menu: ")
        user_input = int(input("1 - VistaVision (1.85), 2 - CinemaScope (2.35), 3 - European WideScreen (1.66), 4 - Academy (1.37) "))
        if user_input in VALID_INPUTS:
            print("You selected: " + ASPECT_RATIO_KEY[user_input] + "!\nLoading Image . . .")
            user_aspect_selection = ASPECT_RATIO[ASPECT_RATIO_KEY[user_input]]
            contrast_image = enhance_contrast()
            cinemized_image = add_black_bars(contrast_image, user_aspect_selection)
            cinemized_image.show()
            cinemized_image.pil_image.save('my_cinemized_picture.jpg')
            valid_input = True
        else:
            print(
                "\nOops! We can't understand your request. You'll need to type in the corresponding number, i.e. 1, 2, 3 or 4 \n")

def enhance_contrast():
    # read the image
    image = Image.open(IMAGE)

    # image brightness enhancer
    enhancer = ImageEnhance.Contrast(image)

    image_output = enhancer.enhance(CONTRAST_FACTOR)
    image_output.save('contrast-image.png')
    contrast_image = 'contrast-image.png'
    return contrast_image

def add_black_bars(contrast_image, aspect_ratio):
    contrast_image = SimpleImage(contrast_image)

    final_image = SimpleImage.blank(contrast_image.width, contrast_image.height)

    # the below equation is derived from a simple proportion of the image's actual width and height vs. the aspect ratio selected
    # The initial equation accounts for the width divided by the total height of image with two black bars subtracted.
    # When we isolate the "black_bar", we get the following formula:
    black_bar = (contrast_image.height * aspect_ratio - contrast_image.width) / 3.7

    for y in range(contrast_image.height):
        for x in range(contrast_image.width):
            pixel = contrast_image.get_pixel(x, y)
            if y <= black_bar or y >= contrast_image.height - black_bar:
                pixel.red = pixel.green = pixel.blue = 0
                final_image.set_pixel(x, y, pixel)
            else:
                final_image.set_pixel(x, y, pixel)

    return final_image

if __name__ == '__main__':
    main()