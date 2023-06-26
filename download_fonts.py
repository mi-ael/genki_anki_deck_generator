from google_drive_downloader import GoogleDriveDownloader as gdd

# https://drive.google.com/file/d/1juEAFPHoF4D8S1CCbARFuiWUX6OYJsU-/view?usp=sharing
gdd.download_file_from_google_drive(file_id='1juEAFPHoF4D8S1CCbARFuiWUX6OYJsU-',
                                    dest_path='./data/fonts/_SourceHanSans-Regular.woff2')
