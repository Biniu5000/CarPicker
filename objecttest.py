import tempfile
from bing_image_downloader import downloader
import time

with tempfile.TemporaryDirectory(dir='images/') as tmpdirname:
    downloader.download("blud thinks he's on the team", limit=1, output_dir=f'{tmpdirname}/',
                        adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    time.sleep(5)
    print('created temporary directory', tmpdirname)
