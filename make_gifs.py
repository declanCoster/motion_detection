import os
import imageio

folders = ['diffs', 'selected', 'threshold_diffs']

'''
https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
'''

for folder in folders:
    files = sorted(os.listdir(folder))
    imgs = []
    for file in files:
        imgs.append(imageio.imread(folder + '/' +file))
    imageio.mimsave(folder + '.gif', imgs)