#!/usr/bin/env python3
import argparse
import os
import urllib.request
import math
import random
from html.parser import HTMLParser
import traceback

# function getNewsc(){
#     $("#suijisc img").attr("class","donghua");
#     $.get("/chaxun/shicirand/?i="+Math.floor(Math.random()*10000+1), function (data, status) {
#         if (status == 'success') {
#             $("#suijiajax").html(data);
#             $("#suijisc img").attr("class","");
#         }
#     });
#     $("#suijiajax").load("/chaxun/shicirand/?i="+Math.floor(Math.random()*10000+1));
# }
import subprocess

URL = 'http://www.shicimingju.com/chaxun/shicirand/?i='
CMD_GIT_ADD_ALL = 'git add -A'
CMD_GIT_COMMIT = 'git commit -m "%s"'
CMD_GIT_PUSH = 'git push origin %s'
MASTER_BRANCH = 'master'


class ParseContent(HTMLParser):
    def error(self, message):
        print('error: %s' % message)

    def __init__(self):
        HTMLParser.__init__(self)
        self.content = []
        self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for (var, value) in attrs:
                if var == 'class' and value == 'suijineirong':
                    self.flag = True
                    break

    def handle_data(self, data):
        if self.flag:
            self.content.append(data)
            return

    def handle_endtag(self, tag):
        if self.flag and tag == 'div':
            self.flag = False


def rand_msg():
    shici_id = int(math.floor(random.random() * 10000 + 1))
    g = urllib.request.urlopen(URL + str(shici_id))

    content = g.read().decode('utf-8')
    parser = ParseContent()
    parser.feed(content)
    return parser.content[random.randint(0, len(parser.content) - 1)]


def run_cmd(cmd, show_msg=False):
    print(cmd)
    if not show_msg:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        rc = p.returncode
        if rc == 0:
            return out
        else:
            print('return code is %d' % rc)
            raise RuntimeError(out)
    else:
        p = subprocess.Popen(cmd, shell=True)
        out, err = p.communicate()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    try:
        arg_parser.add_argument('-m', type=str, default=rand_msg(), metavar='<msg>',
                                help='Use the given <msg> as the commit message')
        arg_parser.add_argument('-b', type=str, default=MASTER_BRANCH, metavar='<brch>', help='push to branch <brch>')
        msg = arg_parser.parse_args().m.strip("。，？、 ,.?'\"")
        branch = arg_parser.parse_args().b
        # print(msg)
        run_cmd(CMD_GIT_ADD_ALL)
        run_cmd(CMD_GIT_COMMIT % msg)
        run_cmd(CMD_GIT_PUSH % branch, True)
    except Exception as err:
        print(traceback.format_exc())
        exit(-1)
    exit(0)
