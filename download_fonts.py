from google_drive_downloader import GoogleDriveDownloader as gdd

# https://drive.google.com/file/d/1BW6v1gTps7NTl8Zvg9D4C5pjbyrpCu63/view?usp=sharing
gdd.download_file_from_google_drive(file_id='1BW6v1gTps7NTl8Zvg9D4C5pjbyrpCu63',
                                    dest_path='./data/fonts/_NotoSansCJKjp-Regular.woff2')
