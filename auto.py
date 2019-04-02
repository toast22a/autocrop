import glob
from os import mkdir
from os.path import basename

import cv2
from tqdm import tqdm

CASCADE_PATH = \
    'haarcascade_frontalface_default.xml'
BUFFER_PCT = 1 # Percentage of the rectangle bounding the face detected

OUT_WIDTH_PX = 140
OUT_HEIGHT_PX = 200
out_ratio = OUT_WIDTH_PX / OUT_HEIGHT_PX

cascade = cv2.CascadeClassifier(CASCADE_PATH)

err_count = 0

# Creates folders if they don't exist
try:
    mkdir('raw')
except:
    pass

try:
    mkdir('cropped')
except:
    pass

with open('log.txt', 'w') as log_file:
    for img_path in tqdm(glob.glob('raw/*')):
        img_path_basename = basename(img_path)

        img_in = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)

        faces, levels, weights = cascade.detectMultiScale3(
            img_gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels=True
        )        

        try:
            # Select the detection with the highest weight
            x, y, w, h = sorted([pair for pair in zip(weights, faces)], key=lambda x : x[0], reverse=True)[0][1]

            x_buf = int(w*BUFFER_PCT/2)
            y_buf = int(h*BUFFER_PCT/2)
            x = max(x - x_buf, 0)
            y = max(y - y_buf, 0)

            w = w + x_buf*2
            if w - x > img_in.shape[1]:
                w = img_in.shape[1] - x

            h = int(w/out_ratio)
            if h - y > img_in.shape[0]:
                h = img_in.shape[0] - y

            new_w = int(h*out_ratio)
            if (new_w < w):
                x = x + int((w - new_w) / 2)
            w = new_w

            img_out = img_in[y:y+h, x:x+w]
            img_out_small = cv2.resize(img_out, (OUT_WIDTH_PX, OUT_HEIGHT_PX))

            cv2.imwrite('cropped/{}'.format(img_path_basename), img_out_small)
        except Exception as ex:
            cv2.imwrite('cropped/{}'.format(img_path_basename), img_in)
            log_file.write('{}: {}\n'.format(img_path_basename, ex))
            err_count += 1

if (err_count > 0):
    print('{} errors -- please check log file at log.txt'.format(err_count))
