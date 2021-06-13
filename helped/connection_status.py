# Importing Necessary Modules
import requests
import shutil


class Network:
    def internet(self):
        try:
            r = requests.get("https://farmzon-abdcb.firebaseio.com/", stream=True)
            return True
        except:
            return False


# Set up the image URL and filename
class Cache_local:
    def Cache(self, url, id):
        image_url = url
        filename = image_url.split("/")[-1]
        filename = filename + "_" + id + ".png"
        r = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            filename = "helped/" + filename
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', filename)
            return filename
        else:
            print('Image Couldn\'t be retreived')
            return False
