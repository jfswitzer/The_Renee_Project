from PIL import Image
import time
def lambda_handler(event,context):
    start = time.time()
    im = Image.open(r"input.jpg")
    width, height = im.size
    newsize = (4 * width, 6 * height)
    im2 = im.resize(newsize)
    im2.save("resized.jpg")
    total = time.time() - start
    return {
        'statusCode': 200,
        'body': json.dumps(f'{total}')
    }
