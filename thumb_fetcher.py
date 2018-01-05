from urllib.parse import urlsplit
import json
import base64
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


# If True shows you the thumbnail and asks you wether you want to change or not each time
# May not work in some systems
show_thumbnail_mode=False


# If True downloaded thumbnails will be embedded into bookmarks file
embed_thumbnails=False


# Make sure the names you put in following lines is exactly the same as that in speed dials

selective=False
# Enter the names of speed dials you want to skip changing the thumbnail, seperated by comma
# if there is no such speed dial just leave it blank
skip=['Vivaldi','Vivaldi Community']

# Uncomment next line if you want to change thumbnails of only selective speeddials (Backspace the #)

#selective=True

# If selective is True enter the names of all speed dials you want to change the thumbnails for seperated by comma in selections
selections=['codechef.com/','spoj.com']



def recurser(recurse_val):
    for val in recurse_val:
        # if 'children' tag not present then it is not a folder
        if not 'children' in val:
            if selective is False and val['name'] in skip:
                print (val['name'] + " found in skip so skipping")
                continue
            if selective is True and val['name'] not in selections:
                print(val['name']+" not found in selections")
                continue

            domain = "{0.scheme}://{0.netloc}/".format(urlsplit(val['url']))
            try:
                img = Image.open(
                    BytesIO(urllib.request.urlopen('https://logo-core.clearbit.com/' + domain + '?size=440').read()))
                img = resizeimage.resize_contain(img, [440, 360])
                if show_thumbnail_mode is False:
                    img.save('xyz.png', img.format)
                    with open('xyz.png', "rb") as bfile:
                        s = bfile.read()
                    up_time = str(int(time.time()))
                    sql = "INSERT OR REPLACE INTO thumbnails(thumbnail,url,url_rank,title,redirects,at_top,load_completed,last_updated,last_forced) VALUES(?,?,?,?,?,?,?,?,?)"
                    cur.execute(sql, (
                        s, "http://bookmark_thumbnail/" + str(val['id']), '-1', '',
                        'http://bookmark_thumbnail/' + str(val['id']), '1', '1', up_time, up_time))
                    if embed_thumbnails:
                         meta = {'Thumbnail': '' + encode_thumb('xyz.png')}
                    else:
                        meta = {
                            'Thumbnail': 'chrome://thumb/' + 'http://bookmark_thumbnail/' + str(val['id']) + "?" + up_time}
                    val['meta_info'] = meta
                    print("Thumbnail temporarily changed for " + val['url'])
                else:
                    print("Opening thumbnail for "+val['name']+"\nPlease wait while image file opens")
                    img.show()
                    x=input("Enter Y for changing, enter anything else for not\n")
                    if x is 'Y' or x is'y':
                        img.save('xyz.png', img.format)
                        with open('xyz.png', "rb") as bfile:
                            s = bfile.read()
                        up_time = str(int(time.time()))
                        sql = "INSERT OR REPLACE INTO thumbnails(thumbnail,url,url_rank,title,redirects,at_top,load_completed,last_updated,last_forced) VALUES(?,?,?,?,?,?,?,?,?)"
                        cur.execute(sql, (
                            s, "http://bookmark_thumbnail/" + str(val['id']), '-1', '',
                            'http://bookmark_thumbnail/' + str(val['id']), '1', '1', up_time, up_time))
                        if embed_thumbnails:
                            meta = {'Thumbnail': '' + encode_thumb('xyz.png')}
                        else:
                            meta = {
                                'Thumbnail': 'chrome://thumb/' + 'http://bookmark_thumbnail/' + str(
                                    val['id']) + "?" + up_time}
                        val['meta_info'] = meta
                        print("Thumbnail temporarily changed for " + val['url'])
                    else:
                        print("Thumbnail not changed")

            except:
                print("Sorry could not load thumbnail for " + val['url'])
        else:
            # if it is a folder then recursing
            if len(val['children'])!=0:
                recurser(val['children'])

def encode_thumb(filename):
    with open(filename, 'rb') as thumbnail_file: # open binary file in read mode
        image_read = thumbnail_file.read()
    image_64_encode = base64.encodebytes(image_read)
    result = image_64_encode.decode().replace('\n', '')
    return ''.join(['data:image/png;base64,', result])


def change_thumb():
    with open(bookmark_path, encoding="UTF-8") as jfile:
        bookmarks = json.load(jfile)
    bookmark_bar_contents = bookmarks["roots"]["bookmark_bar"]["children"]
    #checking if bookmark content is an Active speeddial or not
    for i in bookmark_bar_contents:
        if 'meta_info' in i:
            if 'Speeddial' in i['meta_info']:
                if i['meta_info']['Speeddial']=='true':
                    recurser(i['children'])
    try:
        #commiting changes
        conn.commit()
        conn.close()
        with open(bookmark_path, 'w') as bmk:
            json.dump(bookmarks, bmk)
        print("All changes commited")
    except:
        print("There was an error. Kindly close all instances of vivaldi if open. All changes reverted")


def cleanup():
    if os.path.isfile('xyz.png'):
        os.remove('xyz.png')


def startup():
    if not os.path.isfile(bookmark_path):
        print("Bookmark file not found at the defined path " + bookmark_path)
    elif not os.path.isfile(top_sites_path):
        print("Top Sites file not found at the defined path " + top_sites_path)
    else:
        global conn,cur
        conn = sqlite3.connect(top_sites_path)
        cur = conn.cursor()
        shutil.copy(bookmark_path,os.getcwd())
        shutil.copy(top_sites_path,os.getcwd())
        change_thumb()
        cleanup()
        print("Done")

if __name__ == '__main__':
    startup()
