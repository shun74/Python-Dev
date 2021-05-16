import os
import io
from PIL import Image, ImageDraw
from google.cloud import vision

class Scan():
    image_path = ""
    output_path = ""
    dictionary = []

    def __init__(self,image_path=None,output_path=None,dictionary=[]):
        self.image_path = image_path
        self.output_path = output_path
        self.dictionary = dictionary
        
    def get_annotations(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image_path, 'rb') as image:
            content = image.read()
        vision_image = vision.Image(content=content)
        response = client.text_detection(image=vision_image)
        return response.text_annotations
    
    def search_dictionary(self,annotations=None):
        descriptions = [data.description for data in annotations]
        searched_descriptions = []
        flags = [False] * len(descriptions)
        for i,text in enumerate(descriptions):
            for j in range(len(descriptions) - i - 1):
                for word in self.dictionary:
                    if text == word:
                        searched_descriptions.append(text)
                        for k in range(j+1):
                            flags[i+k] = True
                text += descriptions[i+j+1]
        return flags, searched_descriptions
    
    def redraw_image(self,annotations=None,flags=[]):
        vertices = [data.bounding_poly for data in annotations]
        im = Image.open(self.image_path)
        draw = ImageDraw.Draw(im)
        for i, flag in enumerate(flags):
            if flag == True:
                box = [(vertices[i].vertices[2].x, vertices[i].vertices[2].y), (vertices[i].vertices[3].x, vertices[i].vertices[3].y)]
                draw.line((box[0], box[1]), width=2, fill='#00ff00')
        try:
            im.save(self.output_path)
            return True
        except:
            return False
        
if __name__ == "__main__":
    
    cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

    scan = Scan(image_path="Image/sample1.jpg",output_path="Image/sample1_scan.jpg",dictionary=["酸","この表示","安藤"])
    annotations = scan.get_annotations()
    flags, searched_descriptions = scan.search_dictionary(annotations)
    if scan.redraw_image(annotations,flags):
        print("scan is completed.")
        print(searched_descriptions)
    else:
        print("scan is failed")
