import os
import sys
import http.server
import datetime
from glob import glob
import subprocess
import cgi

import rarfile

from config import cfgoptions


def toconsole(consolestring):
    print(datetime.datetime.now().isoformat() + '  ' + consolestring)


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
            toconsole('mkv aborting scan of: ' + dirname + ' (no media files found to analyze)')
            return False
        for basefile in mediafiles:
            basefiles.append(os.path.split(basefile)[1])
            return basefiles
    else:
        mediafiles.sort()
        basefiles.append(os.path.split(mediafiles[0])[1])
        rarname = os.path.split(mediafiles[0])
        filelist = getrarlist(mediafiles[0])
        if len(filelist) < 1:
            toconsole('rar aborting scan of: ' + dirname + ' (no media files found to analyze)')
            return False
        return basefiles


def handlepath(path, http, preset):
    toconsole(path)
    if not os.path.isdir(cfgoptions.pathname + path):
        toconsole('not a dir :(')
        return
    mediafiles = findmedia(cfgoptions.pathname + path)
    if not mediafiles:
        toconsole('no mediafiles :(')
        return
    cmd = [cfgoptions.vlc, cfgoptions.pathname + path + '\\' + mediafiles[0], '-I dummy', '--dummy-quiet', '--sout']
    if preset == '360p':
        cmd.append(cfgoptions.preset_360p)
    elif preset == '540p':
        cmd.append(cfgoptions.preset_540p)
    elif preset == '720p':
        cmd.append(cfgoptions.preset_720p)
    elif preset == '1080p':
        cmd.append(cfgoptions.preset_1080p)
    else:
        cmd.append(cfgoptions.preset_360p)
    cmd.append('vlc://quit')
    print(cmd)
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=os.environ)
    #http.wfile.write(handle.stdout.read(188))
    # for out in handle.stdout.read(188):
    count = 0
    bufsize = 200
    buffer = None
    # handle.stdout.readable()
    while handle.poll() is None:
        # print(struct.pack('>I', out))
        if count is 0:
            count += 1
            try:
                buffer = handle.stdout.read(188)
            except:
                handle.kill()
                return
        elif count is bufsize:
            count += 1
            try:
                http.wfile.write(buffer)
                buffer = None
            except:
                handle.kill()
                return
        elif count > bufsize:
            if count % 2:
                try:
                    buffer = handle.stdout.read(188)
                except:
                    handle.kill()
                    return
            else:
                try:
                    http.wfile.write(buffer)
                    buffer = None
                except:
                    handle.kill()
                    return
            count += 1
        else:
            count += 1
            try:
                buffer += handle.stdout.read(188)
            except:
                handle.kill()
                return
    handle.kill()
    #http.close_connection
    return

def choice(http):
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
        http.wfile.write(bytes(option, encoding='utf-8'))
    return


class MyHandler(http.server.BaseHTTPRequestHandler):
    preset = '360p'
    def do_GET(self):
        video = False
        lbjs = False
        binary = False
        # print(self.path[7:])
        if self.path[1:7] == 'videos':
            self.send_response(200)
            self.send_header("Content-type", "video/x-flv")
            video = True
        elif self.path[1:5] == 'lbjs':
            self.send_response(200)
            if self.path[-2:1] == 'j':
                self.send_header("Content-type", "application/javascript")
            else:
                self.send_header("Content-type", "application/x-shockwave-flash")
                binary = True
            lbjs = True
        elif len(self.path) == 1:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.end_headers()
        if video:
            handlepath(self.path.replace('/', '\\')[8:-5], self, self.path[-4:])
            return
        if lbjs:
            with open(self.path[1:], mode='rb') as js:
                if not binary:
                    self.wfile.write(js.read().encode(encoding='utf-8'))
                else:
                    self.wfile.write(js.read())
            return
        else:
            with open('choiceheader.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
            choice(self)
            with open('choicefooter.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        return


    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})
        # self.preset = form['preset'].value
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open('streamheader.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        video = self.headers.get('Referer') + 'videos/' + form['video'].value + '/' + form['preset'].value
        self.wfile.write(bytes(video, encoding='utf-8'))
        with open('streamfooter.html') as html:
                self.wfile.write(html.read().encode(encoding='utf-8'))
        return


def main():
    try:
        server = http.server.HTTPServer(('192.168.10.40', 12000), MyHandler)
        print('Started http server')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    main()