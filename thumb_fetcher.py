from urllib.parse import urlsplit
import json
import sqlite3
import time
import shutil
import os
from PIL import Image
from resizeimage import resizeimage
import urllib.request
from io import BytesIO

bookmark_path="C:/Users/Gotham/AppData/Local/Vivaldi/User Data/Default/Bookmarks"
top_sites_path="C:/Users/Gotham/AppData/Local/Vivaldi/User Data/Default/Top Sites"
conn = sqlite3.connect(top_sites_path)
cur = conn.cursor()

def recurser(recurse_val):
    for val in recurse_val:
        if not 'children' in val:
            domain = "{0.scheme}://{0.netloc}/".format(urlsplit(val['url']))
            try:
                img = Image.open(
                    BytesIO(urllib.request.urlopen('https://logo-core.clearbit.com/' + domain + '?size=440').read()))
                img = resizeimage.resize_contain(img, [440, 360])
                img.save('xyz.png', img.format)
                with open('xyz.png', "rb") as bfile:
                    s = bfile.read()
                up_time = str(int(time.time()))
                sql = "INSERT OR REPLACE INTO thumbnails(thumbnail,url,url_rank,title,redirects,at_top,load_completed,last_updated,last_forced) VALUES(?,?,?,?,?,?,?,?,?)"
                cur.execute(sql, (
                    s, "http://bookmark_thumbnail/" + str(val['id']), '-1', '',
                    'http://bookmark_thumbnail/' + str(val['id']), '1', '1', up_time, up_time))
                meta = {'Thumbnail': 'chrome://thumb/' + 'http://bookmark_thumbnail/' + str(val['id']) + "?" + up_time}
                val['meta_info'] = meta
                print("Thumbnail temporarily changed for " + val['url'])
            except:
                print("Sorry could not load thumbnail for " + val['url'])
        else:
            if len(val['children'])!=0:
                recurser(val['children'])


def change_thumb():
    with open(bookmark_path, encoding="UTF-8") as jfile:
        bookmarks = json.load(jfile)
    speeddial = bookmarks["roots"]["bookmark_bar"]["children"][0]["children"]
    recurser(speeddial)
    try:
        with open(bookmark_path, 'w') as bmk:
            json.dump(bookmarks, bmk)
        conn.commit()
        conn.close()
        print("All changes commited")
    except:
        print("There was an error. Kindly close all instances of vivaldi if open. All changes reverted")



def startup():
    if not os.path.isfile(bookmark_path):
        print("Bookmark file not found at the defined path "+bookmark_path)
    elif not os.path.isfile(top_sites_path):
        print("Top Sites file not found at the defined path " + top_sites_path)
    else:
        shutil.copy(bookmark_path,os.getcwd())
        shutil.copy(top_sites_path,os.getcwd())
        change_thumb()
        if os.path.isfile('xyz.png'):
            os.remove('xyz.png')
        print("Done")

if __name__ == '__main__':
    startup()