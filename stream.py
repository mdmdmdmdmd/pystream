import os
import http.server
from socketserver import ThreadingMixIn
from glob import glob
import subprocess
import cgi
import json
import urllib.parse
import shlex

import rarfile

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
        filelist = getrarlist(mediafiles[0])
        if len(filelist) < 1:
            return False
        return basefiles


class ThreadingSimpleServer(ThreadingMixIn, http.server.HTTPServer):
    pass


class MyHandler(http.server.BaseHTTPRequestHandler):
    def _handlepath(self, path, preset):
        mediafiles = findmedia(cfgoptions.pathname + path)
        if not mediafiles:
            return
        cmd = cfgoptions.extract + ' ' + cfgoptions.pathname + path + '/' + mediafiles[0]
        cmd = shlex.split(cmd, posix=False)
        print(cmd)
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
        print(cmd)
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

    def _choice(self):
        walklist = os.walk(cfgoptions.pathname)
        dirlist = []
        for root, dirs, files in walklist:
            for direntry in dirs:
                if direntry[0:1] != '.':
                    dirlist.append(direntry)
            break
        dirlist.sort()
        for direntry in dirlist:
            option = '<option value="' + direntry + '">' + direntry + '</option>'
            self.wfile.write(bytes(option, encoding='utf-8'))
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
            walklist = os.walk(cfgoptions.pathname)
            dirlist = []
            for root, dirs, files in walklist:
                for direntry in dirs:
                    if direntry[0:1] != '.':
                        dirlist.append(direntry)
                break
            dirlist.sort()
            json_dict['count'] = len(dirlist)
            for direntry in dirlist:
                json_dict['list'].append(direntry)
            self.wfile.write(bytes(json.dumps(json_dict), encoding='utf-8'))
        elif method == 'get_preset_json':
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
            json_dict = [low, high, 'best', 'bestsurround']
            self.wfile.write(bytes(json.dumps(json_dict), encoding='utf-8'))
        return

    def do_GET(self):
        video = False
        flash = False
        binary = False
        api = False
        if self.path[1:7] == 'videos':
            self.send_response(200)
            self.send_header("Content-type", "video/flv")
            video = True
        elif self.path[1:6] == 'flash':
            self.send_response(200)
            if self.path[-2:1] == 'j':
                self.send_header("Content-type", "application/javascript")
            else:
                self.send_header("Content-type", "application/x-shockwave-flash")
                binary = True
            flash = True
        elif self.path[1:4] == 'api':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            api = True
        elif len(self.path) == 1:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.end_headers()
        if video:
            url_elements = urllib.parse.urlparse('http://foo' + self.path)
            preset = urllib.parse.parse_qs(url_elements.query)['preset'][0]
            self._handlepath(url_elements.path[8:], preset)
            return
        elif flash:
            with open(self.path[1:], mode='rb') as js:
                if not binary:
                    self.wfile.write(js.read())
                else:
                    self.wfile.write(js.read())
            return
        elif api:
            self._handleapi(self.path[5:])
        else:
            with open('choiceheader.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
            self._choice()
            with open('choicefooter.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open('streamheader.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        video = self.headers.get('Referer') + 'videos/' + form['video'].value + '?preset=' + form['preset'].value
        self.wfile.write(bytes(video, encoding='utf-8'))
        with open('streamfooter.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        return

    def do_HEAD(self):
        if self.path[1:7] == 'videos':
            self.send_response(200)
            self.send_header("Content-type", "video/flv")
            self.end_headers()
        return

def main():
    server = ThreadingSimpleServer((cfgoptions.host, cfgoptions.port), MyHandler)
    print('Started http server')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    main()
