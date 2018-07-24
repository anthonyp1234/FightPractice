Hi Everyone, 

This is a simple kodi addon I wrote (adapted from the example).
I am using it as a tool to help me practice my martial arts.
Basically it scrapes a local directory and creates folders based on the subdirectories in it.
Then selecting the category (category taken from the folder names) it plays a random video from that folder.

So for example, I have in the folder, subfolders names "Stetching" "BJJ" and "Sparring"

Within each subfolder I have a number of short video related to the subject.
**Update** - Alternatively you can have a/many text files containing on each new line a youtube video link, or playlist.
When I want to practice/do one of them I select the icon in the kodi addon, and it plays one at random for me.

Currently the folder it looks for is at:
"/media/storage/fight_practice/"


but you can change that by editing line 
media_directory = "/media/storage/fight_practice/"



