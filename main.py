import requests
from download_img import download_image
import os
import random
from dotenv import load_dotenv

PARAMS = {
            'access_token': os.getenv('VK_XKCD_POST_KEY'),
            'group_id': os.getenv('GROUP_ID'),
            'v': 5.103,
         }


def get_current_image_num():

    response = requests.get('https://xkcd.com/info.0.json')
    
    if response.ok:
        return response.json()['num']


def get_image(img_num):

    response = requests.get(f'https://xkcd.com/{img_num}/info.0.json')
    
    if response.ok:
        response_xkcd = response.json()
        return download_image(response_xkcd['img'], response_xkcd['num']), response_xkcd['alt']


def get_url():

    response = requests.get(
        'https://api.vk.com/method/photos.getWallUploadServer', params=PARAMS)
        
    if response.json().get('response', False):
        return response.json()['response']['upload_url']
    else:
        return response.json()['error']['error_msg']


def upload_image(file_name):

    with open(file_name, 'rb') as file:
        files = {
            'photo': file,
                }

        response = requests.post(get_url(), files=files)
    return response.json()


def save_image(data_for_save_image):

    params_to_save_image = PARAMS.copy()
    params_to_save_image.update({
        'server': data_for_save_image['server'],
        'photo': data_for_save_image['photo'],
        'hash': data_for_save_image['hash'],

                                })

    response = requests.post(
        'https://api.vk.com/method/photos.saveWallPhoto', params=params_to_save_image)

    if response.json().get('response', False):
        response_for_save_image = response.json()['response'][0]
        return response_for_save_image['owner_id'], response_for_save_image['id']
    else:
        return response.json()['error']['error_msg']


def make_post(owner_id, image_id, message):

    params_to_post = PARAMS.copy()
    params_to_post.update({
        'owner_id': -int(PARAMS['group_id']),
        'from_group': 1,
        'attachments': f'photo{owner_id}_{image_id}',
        'message': message
                          })

    response = requests.get(
        'https://api.vk.com/method/wall.post', params=params_to_post)

    if response.json().get('response', False):
        return "Пост успешно размещен"
    else:
        return response.json()['error']['error_msg']


def main():

    load_dotenv()
    img_name, message = get_image(random.randint(1, get_current_image_num()))
    data_for_save_image = upload_image(img_name)
    owner_id, image_id = save_image(data_for_save_image)
    print(make_post(owner_id, image_id, message))
    os.remove(img_name)


if __name__ == "__main__":
    main()
