import urllib
import requests
import os
from pytube import YouTube 

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def download_url(url,dir=os.path.join(os.getcwd(),'Data')):
    
    if "youtube" in url:
        
        try: 
            # object creation using YouTube
            # which was imported in the beginning 
            yt = YouTube(url) 
            stream = yt.streams.get_by_resolution("360p")
            stream.download(output_path=dir)
        except: 
            print("Connection Error") #to handle exception 
    
    else:
    
        r = requests.get(url, allow_redirects=True)
        print(r.headers.get('content-type'))
        
        if is_downloadable(url):
            file_name = url.split('/')[-1]
            u = urllib.request.urlopen(url)
            f = open(os.path.join(dir,file_name), 'wb')
            meta = u.info()
            file_size  = int(meta.get("Content-Length"))
            print ("Downloading: %s Bytes: %s" % (file_name, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print(status)

            f.close()
        
if __name__=="__main__":
    download_url("https://www.youtube.com/watch?v=j5XdY5wkVTA&list=PLUl4u3cNGP63Z979ri_UXXk_1zrvrF77Q")