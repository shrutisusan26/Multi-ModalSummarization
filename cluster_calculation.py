def calc_clusters(duration,fps):
    total_frames = duration*fps
    
    if duration<=300:
        vc_clusters = total_frames//1000
    
    elif duration>300 and duration<=900:
        vc_clusters = total_frames//1500
        
    elif duration>900 and duration<=1800:
        vc_clusters = total_frames//2400
    
    elif duration>1800 and duration<=2700:
        vc_clusters = total_frames//3000
    
    else:
        vc_clusters = total_frames/3600
        
    text_clusters = int(vc_clusters*2.5)
    
    return vc_clusters,text_clusters
        