import requests
import os


def download_image(url, name):
    image_dir = os.path.normcase('.')
    os.makedirs(image_dir, exist_ok=True)
    img_response = requests.get(url)
    exstension = url.rsplit('.')[-1]
    fname = f'{image_dir}/{name}.{exstension}'
    with open(fname, 'wb') as img:
        img.write(img_response.content)
    return fname


if __name__ == "__main__":
    download_image(
        'https://media.stsci.edu/uploads/image_file/image_attachment/1/full_jpg.jpg', 'NASA')
