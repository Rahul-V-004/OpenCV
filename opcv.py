
import cv2

class imconverter:
    def __init__(self,image_path):
        self.image_path=image_path
        try:
            self.color_image = cv2.imread(image_path)
        except:
            print("An error occured please provide different image!!!")

    def convert(self):
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('output_grey_image.jpg', gray_image)
        inverted_image = cv2.bitwise_not(gray_image)
        cv2.imwrite('inverted_image.jpg', inverted_image)
        blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
        pencil_sketch = cv2.divide(inverted_image, blurred_image, scale=246.0)       
        cv2.imwrite('pencil_sketch.jpg',pencil_sketch)

