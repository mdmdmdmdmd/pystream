import os
import http.server
from socketserver import ThreadingMixIn
from glob import glob
import subprocess
import json
import urllib.parse
import shlex
# import ssl

import rarfile

from auth import read_db
from config import cfgoptions


def getrarlist(rarname):
    rarfile.NEED_COMMENTS = 0
    filelist = []
    if not rarfile.is_rarfile(rarname):
        return filelist
    rararc = rarfile.RarFile(rarname)
    for rarentry in rararc.infolist():
        filelist.append(rarentry.filename)
    return filelist

def findmedia(dirname):
    basefiles = []
    mediafiles = glob(dirname + '/*.rar')
    if len(mediafiles) < 1:
        mediafiles = glob(dirname + '/*.mkv')
        if len(mediafiles) < 1:
            return False
        for basefile in mediafiles:
            basefiles.append(os.path.split(basefile)[1])
            return basefiles
    else:
        mediafiles.sort()
        basefiles.append(os.path.split(mediafiles[0])[1])
        return basefiles


class ThreadingSimpleServer(ThreadingMixIn, http.server.HTTPServer):
    pass


class MyHandler(http.server.BaseHTTPRequestHandler):
    def _handlepath(self, path, preset):
        elements = path.split('/')
        path = elements[1]
        mediafiles = findmedia(cfgoptions.dirs.get(elements[0]) + path)
        if not mediafiles:
            return
        cmd = cfgoptions.extract + ' ' + cfgoptions.dirs.get(elements[0]) + path + '/' + mediafiles[0]
        cmd = shlex.split(cmd, posix=False)
        unrar = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=os.environ)
        cmd = cfgoptions.ffmpeg + ' -i pipe: '
        if preset == 'low':
            cmd += cfgoptions.preset_low
        elif preset == 'high':
            cmd += cfgoptions.preset_high
        elif preset == 'best':
            cmd += cfgoptions.preset_best
        elif preset == 'bestsurround':
            cmd += cfgoptions.preset_best_surround
        elif preset == 'source':
            cmd += cfgoptions.preset_source
        elif preset == 'low1080p':
            cmd += cfgoptions.preset_low_1080p
        elif preset == 'high1080p':
            cmd += cfgoptions.preset_high_1080p
        elif preset == 'low720p':
            cmd += cfgoptions.preset_low_720p
        elif preset == 'high720p':
            cmd += cfgoptions.preset_high_720p
        elif preset == 'lowdvd':
            cmd += cfgoptions.preset_low_dvd
        elif preset == 'highdvd':
            cmd += cfgoptions.preset_high_dvd
        else:
            cmd += cfgoptions.preset_low
        cmd = shlex.split(cmd, posix=False)
        transcode = subprocess.Popen(cmd, stdin=unrar.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=os.environ)
        while transcode.poll() is None:
            try:
                buffer = transcode.stdout.read(188)
                if not buffer:
                    break
                self.wfile.write(buffer)
            except:
                unrar.kill()
                transcode.kill()
                return
        return

    def _handleapi(self, path):
        elements = path.split('/')
        method = elements[0]
        if len(elements) > 1:
            dir = elements[1]
        else:
            dir = ''
        if method == 'get_index_json':
            json_dict = {'count': 0, 'list': []}
            dirlist = []
            if len(dir) > 0:
                walklist = os.walk(cfgoptions.dirs.get(dir))
                for root, dirs, files in walklist:
                    for direntry in dirs:
                        if direntry[0:1] != '.':
                            dirlist.append(direntry)
                    break
            else:
                for entry in cfgoptions.dirs.keys(): dirlist.append(entry)
            dirlist.sort()
            json_dict['count'] = len(dirlist)
            for direntry in dirlist:
                json_dict['list'].append(direntry)
            self.wfile.write(bytes(json.dumps(json_dict), encoding='utf-8'))
        elif method == 'get_preset_json':
            if len(elements) > 2:
                dir = elements[2]
            else:
                dir = ''
            low = 'low'
            high = 'high'
            if '1080p' in dir:
                low += '1080p'
                high += '1080p'
            elif '720p' in dir:
                low += '720p'
                high += '720p'
            elif 'dvdrip' in dir.lower():
                low += 'dvd'
                high += 'dvd'
            json_dict = [low, high, 'best', 'bestsurround', 'source']
            self.wfile.write(bytes(json.dumps(json_dict), encoding='utf-8'))
        return

    def do_GET(self):
        username = self.headers.get('login')
        password = self.headers.get('password')
        if username is not None and password is not None:
            db = read_db()
            if username in db and password == db.get(username):
                if self.path[1:7] == 'videos':
                    self.send_response(200)
                    self.send_header("Content-type", "video/mkv")
                    self.end_headers()
                    url_elements = urllib.parse.urlparse('http://foo' + self.path)
                    preset = urllib.parse.parse_qs(url_elements.query)['preset'][0]
                    self._handlepath(url_elements.path[8:], preset)
                    return
                elif self.path[1:4] == 'api':
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self._handleapi(self.path[5:])
                    return
        self.send_response(404)
        self.end_headers()
        return

    def do_HEAD(self):
        if self.path[1:7] == 'videos':
            self.send_response(200)
            self.send_header("Content-type", "video/mkv")
        else:
            self.send_response(404)
        self.end_headers()
        return

def main():
    server = ThreadingSimpleServer((cfgoptions.host, cfgoptions.port), MyHandler)
    print('Started http server')
    try:
        # server.socket = ssl.wrap_socket (server.socket, keyfile='key.pem', certfile='cert.pem', server_side=True)
        # TODO: figure out why ssl is so slow :(
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    main()
