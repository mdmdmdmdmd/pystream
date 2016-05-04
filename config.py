class CfgOptions():
    pathname = 'z:/'
    ffmpeg = 'd:/apps/FFMPEG/bin/ffmpeg.exe'
    extract = 'UnRAR.exe p -inul'
    host = '192.168.10.40'
    port = 9999
    preset_low = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_high = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_low_1080p = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_high_1080p = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -vf scale=1280:-2 -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_low_720p = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=640:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_high_720p = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_low_dvd = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 500k -minrate 100k -maxrate 500k -bufsize 250k -vf scale=320:-2 -c:a libopus -ac 2 -b:a 80k -f matroska -y pipe:'
    preset_high_dvd = '-c:v libx264 -crf 19 -preset medium -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 1500k -minrate 100k -maxrate 1500k -bufsize 750k -c:a libopus -ac 2 -b:a 96k -f matroska -y pipe:'
    preset_best = '-c:v libx264 -crf 19 -preset faster -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 3500k -minrate 100k -maxrate 3500k -bufsize 1750k -c:a libopus -ac 2 -b:a 128k -f matroska -y pipe:'
    preset_best_surround = '-c:v libx264 -crf 19 -preset faster -tune film -profile:v high -level 4.1 -x264opts keyint=250:nr=90 -b:v 3500k -minrate 100k -maxrate 3500k -bufsize 1750k -c:a libopus -b:a 256k -f matroska -y pipe:'

cfgoptions = CfgOptions()
