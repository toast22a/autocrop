from sys import argv
from os import mkdir
from os.path import basename

def show_help():
    print('Usage: {} <filename of raw image>'.format(argv[0]))

if (len(argv) < 2):
    show_help()
    quit()

import cv2

# Creates folders if they don't exist yet
try:
    mkdir('raw')
except:
    pass

try:
    mkdir('cropped')
except:
    pass

OUT_WIDTH_PX = 140
OUT_HEIGHT_PX = 200
out_ratio = OUT_WIDTH_PX / OUT_HEIGHT_PX

img_path = 'raw/' + argv[1]
img_path_basename = basename(img_path)

selecting = 0
x1 = 0
y1 = 0
x2 = 0
y2 = 0

def mouse_callback(event, local_x, local_y, flags, img):
    global selecting, x1, y1, x2, y2
    if event == cv2.EVENT_LBUTTONDOWN and selecting==0:
        x1 = local_x
        y1 = local_y
        selecting = 1
    elif event == cv2.EVENT_MOUSEMOVE and selecting==1:
        img_clone = img * 1
        x2 = x1 + int((local_y-y1) * out_ratio)
        y2 = local_y
        cv2.rectangle(img_clone, (x1,y1), (x2,y2), (0,255,0), 10)
        cv2.imshow('image', img_clone)
    elif event == cv2.EVENT_LBUTTONDOWN and selecting==1:
        img_clone = img * 1
        x2 = x1 + int((local_y-y1) * out_ratio)
        y2 = local_y
        cv2.rectangle(img_clone, (x1,y1), (x2,y2), (0,255,0), 10)
        cv2.imshow('image', img_clone)
        selecting = 2
    elif event == cv2.EVENT_MOUSEMOVE and selecting==2:
        img_clone = img * 1
        x1 = x1 + (local_x - x2)
        y1 = y1 + (local_y - y2)
        x2 = local_x
        y2 = local_y
        cv2.rectangle(img_clone, (x1,y1), (x2,y2), (0,255,0), 10)
        cv2.imshow('image', img_clone)
    elif event == cv2.EVENT_LBUTTONDOWN and selecting==2:
        selecting = 0
        img_clone = img * 1
        x1 = x1 + (local_x - x2)
        y1 = y1 + (local_y - y2)
        x2 = local_x
        y2 = local_y
        cv2.rectangle(img_clone, (x1,y1), (x2,y2), (0,255,0), 10)
        cv2.imshow('image', img_clone)

img_in = cv2.imread(img_path)
cv2.imshow('image', img_in)
cv2.setMouseCallback('image', mouse_callback, img_in)

key = cv2.waitKey(0) & 0xFF
if key == ord('s') and x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
    img_out = img_in[y1:y2, x1:x2]
    img_out_small = cv2.resize(img_out, (OUT_WIDTH_PX, OUT_HEIGHT_PX))
    cv2.imwrite('cropped/{}'.format(img_path_basename), img_out_small)
