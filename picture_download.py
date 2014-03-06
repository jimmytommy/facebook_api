import urllib
import requests
import configure

class PictureDownload(object):
    """ Class to maintain downloads of every picture I am 
    tagged in on Facebook. """

    PARAMS = {"access_token" : configure.access_token}
    URL = "https://graph.facebook.com/me"

    @classmethod
    def download_pic(klass, url, pic_name):
        full_filename = configure.download_dir + pic_name
        if full_filename[-4:] != ".jpg":
            full_filename += ".jpg"

        print url
        print full_filename
        f = open(full_filename, 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()

    @classmethod
    def download_all_pics(klass):

        params = klass.PARAMS.copy()
        params["fields"] = "photos"
        print "making GET request!"
        r = requests.get(klass.URL, params=params)
        
        if r.status_code != 200:
            print "FAILURE!"
            return r

        resp = r.json()
        print len(resp["photos"]["data"])
        for photo in resp["photos"]["data"]:
            print "name"
            source_url = photo["source"]
            name = photo["name"]

            klass.download_pic(source_url, name)
