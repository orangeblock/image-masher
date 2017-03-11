# image-masher
A simple script to mash images together in horizontal or vertical strips.

-
####Requirements
- Python 2.7
- Pillow 4.0.0  
You can install it via pip: `pip install Pillow`  

####Usage
Feed it a list of files or URLs and it will create a series of "image strips". Which is the visible part of each image depends on its final position in the mashed up image.  
Can be used as a command line script or a library. Use --help to view options for the former.
To use it as a library import the file and call the `mash` method.

####Examples
All arguments except `images` are optional, with sane default values. You can pass in filepaths, URLs or a mix of both.
```
import masher

images = [
 'https://cdn.pixabay.com/photo/2016/03/09/09/18/biking-1245722_1280.jpg',
 'https://cdn.pixabay.com/photo/2016/12/29/22/31/leopard-1939471_1280.jpg',
 'https://cdn.pixabay.com/photo/2014/07/05/16/44/biker-384921_1280.jpg',
 'https://cdn.pixabay.com/photo/2017/02/25/16/31/cityscape-2098170_1280.jpg',
 'https://cdn.pixabay.com/photo/2015/11/16/06/20/baseball-player-1045263_1280.jpg'
]

masher.mash(images, size=(900,900), direction=masher.VERTICAL, save=True, out='.', out_name='mashed')
```
Output in ./mashed.jpg:  
<img src="http://i.imgur.com/QDkyhdZ.jpg" width="300" height="200" />
