import sys
sys.argv = ["x"]
import numpy as np
from PIL import Image

exec(open("/home/sprite/slop-salon-lelia/notes/column_ends.py").read().split("row_counts = ")[0])

s = er + ex
print("rows on x+row=1424:", sorted(er[s == 1424].tolist())[:25])
print("x+row=1420 spacing:", set(np.diff(np.sort(er[s == 1420])).tolist()))

img = np.zeros((H - START, W, 3), np.uint8)
img[m] = (60, 70, 110)
for dr in (-1, 0, 1):
    for dx in (-1, 0, 1):
        rr = np.clip(er - START + dr, 0, img.shape[0] - 1)
        xx = np.clip(ex + dx, 0, W - 1)
        img[rr, xx] = (255, 200, 60)
print("yellow px", int(((img == (255, 200, 60)).all(axis=2)).sum()))
out = "/home/sprite/slop-salon-lelia/assets/rule54_shift1_column_ends.png"
Image.fromarray(img, "RGB").save(out)
print(out, img.shape)
