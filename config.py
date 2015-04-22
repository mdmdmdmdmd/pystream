class CfgOptions():
    pathname = 'z:\\'
    vlc = 'd:\\apps\\vlc\\vlc.exe'
    preset_360p = '#transcode{vcodec=h264,venc=x264{keyint=250,preset=medium,tune=film,level=41,profile=high,vbv-maxrate=500,vbv-bufsize=200,bitrate=500,nr=9000},vb=9000,scale=0.33,acodec=mp4a,channels=2,ab=128,threads=16}:duplicate{dst=std{access=file,mux=ffmpeg{mux=flv},dst=-}}'
    preset_540p = '#transcode{vcodec=h264,venc=x264{keyint=250,preset=medium,tune=film,level=41,profile=high,vbv-maxrate=1200,vbv-bufsize=600,bitrate=1200,nr=1000},vb=9000,scale=0.5,acodec=mp4a,channels=2,ab=128,threads=16}:duplicate{dst=std{access=file,mux=ffmpeg{mux=flv},dst=-}}'
    preset_720p = '#transcode{vcodec=h264,venc=x264{keyint=250,preset=fast,tune=film,level=41,profile=high,vbv-maxrate=1500,vbv-bufsize=700,bitrate=1500,nr=100},vb=9000,scale=0.67,acodec=mp4a,channels=2,ab=192,threads=16}:duplicate{dst=std{access=file,mux=ffmpeg{mux=flv},dst=-}}'
    preset_1080p = '#transcode{vcodec=h264,venc=x264{keyint=250,preset=faster,tune=film,level=41,profile=high,vbv-maxrate=2500,vbv-bufsize=1200,bitrate=2500,nr=100},vb=9000,acodec=mp4a,channels=2,ab=256,threads=16}:duplicate{dst=std{access=file,mux=ffmpeg{mux=flv},dst=-}}'

cfgoptions = CfgOptions()
