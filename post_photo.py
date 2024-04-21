import requests

def post_single_photo(page_id, page_access_token, message, photo_url):
    url = f"https://graph.facebook.com/v18.0/me/photos"
    files = {'upload_file': open(photo_url, 'rb')}
    params = {
        'access_token': page_access_token,
        'message': message,
    }

    try:
        response = requests.post(url, params=params, files=files)
        result = response.json()

        if 'id' in result:
            print(f"Photo posted successfully. Post ID: {result['id']}")
        else:
            print(f"Error posting photo: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
