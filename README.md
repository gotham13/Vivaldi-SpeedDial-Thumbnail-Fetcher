# Vivaldi-SpeedDial-Thumbnail-Fetcher
Automatically fetches and changes the thumbnail of sites in Vivaldi's speed dial.  
vivaldi forum link  
https://forum.vivaldi.net/topic/23414/an-automatic-logo-thumbnail-fetcher-and-changer-for-vivaldi-speeddial


## PREREQUISITES
* Python 3 or above  

## LIBRARIES USED
* python-resize-image


## CONFIGURATION  
* pip install -r requirements.txt
* change the values of the following varialbles in thumb_fetcher.py
* You can change show_thumbnail_mode to True for showing the thumbnails before asking to change or not  
* Also change the values of selection and skip according to need  

| Name | Description | Path |
|------|-------------|---------|
| `top_sites_path` | Stores the path to the "Top Sites" file of Vivaldi which stores the thumbnails. | Windows: `C:/Users/<User>/AppData/Local/Vivaldi/User Data/Default/Top Sites` <br/> OS X: `/Users/<User>/Library/Application Support/Vivaldi/Default/Top Sites` <br/> Linux: `/home/<User>/.config/vivaldi-snapshot/Default/Top Sites` |
| `bookmark_path` | Stores the path to the "Bookmark" file of Vivaldi which stores among other things the bookmark id and its name. | Windows: `C:/Users/<User>/AppData/Local/Vivaldi/User Data/Default/Bookmarks` <br/> OS X: `/Users/<User>/Library/Application Support/Vivaldi/Default/Bookmarks` <br/> Linux: `/home/<User>/.config/vivaldi-snapshot/Default/Bookmarks` |

**Important:**

* You need to replace `<User>` with your own user name.
* When modifying or replacing the paths make sure you only use `/`. You need to replace all backslashes when copying a Windows path from the explorer!

## RUNNING THE SCRIPT
* Close all instances of vivaldi before running the script
* The original files will be backed up in the working directory of the script

## PLEASE NOTE
The thumbnails fetched are twitter thumbnails for the given site. So images might be incorrect in certain cases. As favicons are very small this is the best option right now. Please dont bash me for this.


## EXAMPLE
### BEFORE
![alt text](https://github.com/Gotham13121997/Vivaldi-SpeedDial-Thumbnail-Fetcher/blob/master/pics/cf1.png)  
### RUNNING
![alt text](https://github.com/Gotham13121997/Vivaldi-SpeedDial-Thumbnail-Fetcher/blob/master/pics/cf2.png)  
### AFTER
![alt text](https://github.com/Gotham13121997/Vivaldi-SpeedDial-Thumbnail-Fetcher/blob/master/pics/cf3.png)
