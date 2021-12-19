
import cv2
import uuid

def extractImages(path):
    count = 0
    new_path = path
    new_path = new_path.split('/')
    new_path = new_path[len(new_path)-1]
  

    vidcap = cv2.VideoCapture(f'public/static/youtube/{new_path}')
    success,image = vidcap.read()
    success = True
    generated_images = []
    try:
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*10000))    # added this line 
            success,image = vidcap.read()
            print ('Read a new frame: ', success)
            image_name = str(uuid.uuid4())
            cv2.imwrite( "public/static/thumbnails/%s.jpg" % image_name, image) 
            generated_images.append(f"media/thumbnails/{image_name}.jpg")
            count = count + 1
            if len(generated_images) > 5:
                return generated_images
    except Exception as e:
        print(e)
    
    return generated_images