class CfgOptions():
    dirs = {'1': 'z:/', '2': 'y:/'}
    ffmpeg = 'd:/apps/FFMPEG/bin/ffmpeg.exe'
    extract = 'UnRAR.exe p -inul'
    host = '192.168.10.40'
    port = 9999
    # preset_low = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_low = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    # preset_high = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_high = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    # preset_low_1080p = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_low_1080p = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    # preset_high_1080p = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_high_1080p = '-map 0:v -map 0:a -c:v libx265 -preset faster -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    # preset_low_720p = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_low_720p = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    # preset_high_720p = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_high_720p = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    # preset_low_dvd = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=320:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_low_dvd = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=320:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    # preset_high_dvd = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_high_dvd = '-map 0:v -map 0:a -c:v libx265 -preset medium -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_best = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset faster -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 3500k -minrate 100k -maxrate 3500k -bufsize 1750k -c:a libopus -ac 2 -b:a 128k -f matroska -y pipe:'
    preset_best_surround = '-map 0:v -map 0:a -c:v libx264 -crf 19 -preset faster -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 3500k -minrate 100k -maxrate 3500k -bufsize 1750k -c:a libvorbis -b:a 256k -f matroska -y pipe:'
    preset_source = '-map 0:v -map 0:a -c:v copy -c:a copy -f matroska -y pipe:'

cfgoptions = CfgOptions()
