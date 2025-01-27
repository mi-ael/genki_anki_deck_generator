import gdown
import os

os.makedirs('./data/fonts', exist_ok=True)

# https://drive.google.com/file/d/1BW6v1gTps7NTl8Zvg9D4C5pjbyrpCu63/view?usp=sharing
gdown.download(id='1BW6v1gTps7NTl8Zvg9D4C5pjbyrpCu63', output='./data/fonts/_NotoSansCJKjp-Regular.woff2')
