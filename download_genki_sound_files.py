from google_drive_downloader import GoogleDriveDownloader as gdd

# https://drive.google.com/file/d/1RXnr3nEiv5gFGIQqdMugrETwXu-lsar1/view?usp=share_link
gdd.download_file_from_google_drive(file_id='1RXnr3nEiv5gFGIQqdMugrETwXu-lsar1',
                                    dest_path='./data/genki_1/sound/genki_1_sounds.zip',
                                    unzip=True)

# https://drive.google.com/file/d/1KPkNM85bM4zymzqO-aLWELah-RVM2p3O/view?usp=share_link
gdd.download_file_from_google_drive(file_id='1KPkNM85bM4zymzqO-aLWELah-RVM2p3O',
                                    dest_path='./data/genki_2/sound/genki_2_sounds.zip',
                                    unzip=True)
