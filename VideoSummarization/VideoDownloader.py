from pytube import YouTube 
  
# link of the video to be downloaded 

def dwldyt(link): 
    yt = YouTube(link)
    #Showing details
    print("Title: ",yt.title)
    print("Number of views: ",yt.views)
    print("Length of video: ",yt.length)
    print("Rating of video: ",yt.rating)
    #Getting the highest resolution possible
    ys = yt.streams.get_highest_resolution()

    #Starting download
    print("Downloading...")
    ys.download()
    print("Download completed!!")

if __name__ =="__main__":
    dwldyt("https://www.youtube.com/watch?v=pN3jRihVpGk&list=PLKiU8vyKB6ti1_rUlpZJFdPaxT04sUIoV&index=1")