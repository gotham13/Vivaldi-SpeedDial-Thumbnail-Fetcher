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

bookmark_path="Your-path-for-Bookmark-file"
top_sites_path="Your-path-for-Top Sites-file"

def change_thumb():
    conn = sqlite3.connect(top_sites_path)
    cur = conn.cursor()
    with open(bookmark_path, encoding="UTF-8") as jfile:
        bookmarks = json.load(jfile)
    speeddial = bookmarks["roots"]["bookmark_bar"]["children"][0]["children"]
    ind = 0
    for i in speeddial:
        if not 'children' in i:
            domain = "{0.scheme}://{0.netloc}/".format(urlsplit(i['url']))
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
                    s, "http://bookmark_thumbnail/" + str(i['id']), '-1', '',
                    'http://bookmark_thumbnail/' + str(i['id']), '1', '1', up_time, up_time))
                meta = {'Thumbnail': 'chrome://thumb/' + 'http://bookmark_thumbnail/' + str(i['id']) + "?" + up_time}
                bookmarks["roots"]["bookmark_bar"]["children"][0]["children"][ind]['meta_info'] = meta
                print("Thumbnail temporarily changed for " + i['url'])
            except:
                print("Sorry could not load thumbnail for " + i['url'])

        else:
            ind1 = 0
            for j in i['children']:
                domain = "{0.scheme}://{0.netloc}/".format(urlsplit(j['url']))
                try:
                    img = Image.open(
                        BytesIO(
                            urllib.request.urlopen('https://logo-core.clearbit.com/' + domain + '?size=440').read()))
                    img = resizeimage.resize_contain(img, [440, 360])
                    img.save('xyz.png', img.format)
                    with open('xyz.png', "rb") as bfile:
                        s = bfile.read()
                    up_time = str(int(time.time()))
                    sql = "INSERT OR REPLACE INTO thumbnails(thumbnail,url,url_rank,title,redirects,at_top,load_completed,last_updated,last_forced) VALUES(?,?,?,?,?,?,?,?,?)"
                    cur.execute(sql, (
                        s, "http://bookmark_thumbnail/" + str(j['id']), '-1', '',
                        'http://bookmark_thumbnail/' + str(j['id']), '1', '1', up_time, up_time))
                    meta = {
                        'Thumbnail': 'chrome://thumb/' + 'http://bookmark_thumbnail/' + str(j['id']) + "?" + up_time}
                    bookmarks["roots"]["bookmark_bar"]["children"][0]["children"][ind]['children'][ind1][
                        'meta_info'] = meta
                    print("Thumbnail temporarily changed for " + j['url'])
                except:
                    print("Sorry could not load thumbnail for " + j['url'])
                    pass
                ind1 = ind1 + 1
        ind = ind + 1
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

if __name__ == '__main__':
    startup()