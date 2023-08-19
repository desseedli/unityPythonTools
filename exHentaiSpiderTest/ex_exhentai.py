# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import threading
import ex_head
import re
import os
import time
import tkinter
from pathlib import Path
import json
import playSound

class main_exhentai(object):
    search_word = '?f_cats=1017&f_search='

    def __init__(self):
        self.conut = 0
        self.cookie = self.loadJson()
        self.head = ex_head.random_head()
        self.target = 'https://exhentai.org/'
        self.allresult = []
        self.name = []
        self.pic = []
        self.downloadurl = []
        self.get_torrent = []
        self.num = 5  # 默认5本
        self.url = 'https://exhentai.org/g/1510037/116d2c7e6e/'
        self.flag = True

        self.path = ''
        self.page_num = 0
        self.surl = ''
    def loadJson(self):
        f = open("ex_cookies.json", encoding='utf-8')
        cookie = json.load(f)
        return cookie

    def requester(self, target, classname, type):
        req = requests.get(target, cookies=self.cookie, headers=self.head, timeout=30)
        bf = BeautifulSoup(req.text, "html.parser")
        texts = bf.find_all(type, class_=classname)
        return texts

    def requester_id(self, target, idname, type):
        req = requests.get(target, cookies=self.cookie, headers=self.head, timeout=30)
        bf = BeautifulSoup(req.text, "html.parser")
        texts = bf.find_all(type, id=idname)
        return texts

    def step_getpage_donurl(self):  # 首页
        self.allresult = []
        self.name = []
        self.pic = []
        self.downloadurl = []
        self.get_torrent = []

        texts = self.requester(self.target + main_exhentai.search_word, 'itg gld', 'div')
        self.allresult = re.findall('<a href=\"(https://exhentai.org/g/.*?/.*?/)\">', str(texts))
        print(self.allresult[::2])
        print(len(self.allresult[::2]))

    def step_getdownloadpage(self):
        crt = self.num
        if len(self.allresult[::2]) < crt:
            crt = len(self.allresult[::2])
        if crt >= 25:
            crt = 25
        for cr in range(0, crt):
            texts = self.requester(self.allresult[::2][cr], 'gm', 'div')
            name = re.findall('<div id="gd2"><h1 id="gn">.*?</h1><h1 id="gj">(.*?)</h1></div>', str(texts))
            if name[0] == '':
                name = re.findall('<div id="gd2"><h1 id="gn">(.*?)</h1><h1 id="gj">.*?</h1></div>', str(texts))
            ext = ['?', '*', ':', '\"', '<', '>', '\\', '/', '|']
            for s in ext:  # 干掉非法字符
                name[0] = name[0][:100].replace(s, '')
            script_path = os.path.dirname(os.path.abspath(__file__))
            torrent_folder_path = os.path.join(script_path, 'ex_torrent')
            file = Path(torrent_folder_path + name[0] + '\\' + name[0] + '.jpg')
            if file.is_file():
                print(name[0] + ' 已经存在')
                continue
            downloadurl = re.search('\'https://exhentai.org/gallerytorrents.php?(.*?)\'', str(texts)).group(0).strip(
                '\'').replace(';', '&')
            pic = re.findall(
                '<div style="width:\d+px; height:\d+px; background:transparent url\((.*?)\) no-repeat"></div>',
                str(texts))
            self.downloadurl.append(downloadurl)
            self.name += name
            self.pic += pic
            print('已录入第' + str(cr + 1) + '本')
        print(self.downloadurl)
        print(self.name)
        print(self.pic)

    def step_gettorrent(self):
        print('正在获取种子……')
        a = 0
        for cr in self.downloadurl:
            texts = self.requester(cr, 'stuffbox', 'div')
            result = re.findall('\"https://exhentai.org/torrent/(.*?)/(.*?).torrent\"', str(texts))
            try:
                get_torrent = 'https://exhentai.org/torrent/' + str(result[0][0]) + '/' + str(result[0][1]) + '.torrent'
            except Exception as e:
                print(self.name[a] + '没有下载资源')
                self.get_torrent.append('')
                a += 1
                continue
            else:
                self.get_torrent.append(get_torrent)
                print('获取了第' + str(a + 1) + '本的种子')
            a += 1
        print(self.get_torrent)

    def donwloader(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        torrent_folder_path = os.path.join(script_path, 'ex_torrent')
        if not os.path.exists(torrent_folder_path):
            os.makedirs(torrent_folder_path)
        for cr in range(0, len(self.get_torrent)):
            floder = os.path.join(torrent_folder_path, '(无种)' + self.name[cr] + '\\')
            if self.get_torrent[cr] != '':
                floder = os.path.join(torrent_folder_path, '(有种)' + self.name[cr] + '\\')
            os.makedirs(floder, exist_ok=True)  # 创建路径
            tname = self.name[cr] + '.torrent'
            p = requests.get(self.pic[cr], cookies=self.cookie, headers=self.head)  # 请求图片连接
            with open(floder + self.name[cr] + '.jpg', 'wb') as f:  # 打开并写入准备
                f.write(p.content)
            if self.get_torrent[cr] == '':
                continue
            r = requests.get(self.get_torrent[cr], cookies=self.cookie, headers=self.head)
            with open(floder + tname, 'wb') as f:  # 打开并写入准备
                f.write(r.content)
            print(self.name[cr] + ' 搞定了')
        print('全部搞定')

    def get_book_info(self):  # 自定义下载模块
        texts = self.requester(self.url, 'gdtm', 'div')
        url = re.search('(https://exhentai.org/s/\w+/\d+-1)', str(texts))  # 获得页面
        self.surl = url.group(0)  # page1获得
        print(url)

        page = self.requester(self.url, 'gdt2', 'td')
        pagenum = re.search('<td class="gdt2">(\d+) pages</td>', str(page))  # 获得总页数
        self.page_num = int(pagenum.group(1))
        print(pagenum.group(1))

        name_te = self.requester_id(self.url, 'gn', 'h1')
        book_name = re.search('<h1 id="gn">(.*)</h1>', str(name_te)).group(1)  # 获得名字
        ext = ['?', '*', ':', '\"', '<', '>', '\\', '/', '|']
        for s in ext:  # 删除非法字符
            book_name = book_name.replace(s, '')
        print(book_name)
        script_path = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(script_path, 'ex_book', book_name + '\\')
        self.path = folder

    def create_download_book_dirs(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        res_folder_path = os.path.join(script_path, 'ex_book')
        if not os.path.exists(res_folder_path):
            os.makedirs(res_folder_path)
        os.makedirs(self.path, exist_ok=True)


if __name__ == "__main__":
    tk = tkinter.Tk()  # 创建Tk对象
    tk.title("EXhentai")  # 设置窗口标题
    tk.geometry("550x700")  # 设置窗口尺寸

    me = main_exhentai()


    def check_resumable_download(pagenum, surl, path, modourl):
        index1 = 0
        index2 = 0
        for cr in range(1, pagenum + 1):
            if index1 == 0:
                file = Path(path + str(cr) + '.jpg')
                if file.is_file():
                    print(str(cr) + '图片已存在')
                    index2 = 1
                    continue

            if index2 == 1:
                print('中断处找到了')
                turn = cr // 20
                if cr % 20 == 0:
                    turn -= 1
                newurl = modourl + '/?p=' + str(turn)
                re_search = '(https://exhentai.org/s/\w+/\d+-' + str(cr) + ')'
                texts = me.requester(newurl, 'gdtm', 'div')
                hurl = re.search(re_search, str(texts))
                surl = hurl.group(0)
                index2 = 0

            urls = find_cur_and_next_page_urls(surl)
            while urls is None:
                urls = find_cur_and_next_page_urls(surl)
                time.sleep(1)
            print(urls[1])  # 本页图片
            t = threading.Thread(target=download_pic, args=(urls[1], path, str(cr), surl))
            t.start()
            surl = urls[0]  # 下一页


    def download_pic(url, path, name, surl):
        me.conut += 1
        if me.conut % 2 == 0:
            me.head = ex_head.random_head()  # 更换请求头，防止被杀
            print(me.head)
        try:
            p = requests.get(url, cookies=me.cookie, headers=me.head, timeout=18)  # 请求图片连接
        except requests.exceptions.ConnectionError as e:
            print('超时了，换源中……')
            time.sleep(1)
            req = requests.get(surl, cookies=me.cookie, headers=me.head)  # 换源
            bf = BeautifulSoup(req.text, "html.parser")
            texts = bf.find_all('div', id='i6')
            thing = re.search('\'\d+-\d+\'', str(texts))
            ssurl = surl + '?nl=' + str(thing.group(0)).replace('\'', '')
            sreq = find_cur_and_next_page_urls(ssurl)
            print(sreq[1])
            try:
                sp = requests.get(sreq[1], cookies=me.cookie, headers=me.head, timeout=30)  # 请求图片连接
                with open(path + name + '.jpg', 'wb') as f:
                    f.write(sp.content)
                print('完成第' + name + '张')
            except requests.exceptions.ConnectionError as e:
                print('这张好像下不了……')
        else:
            with open(path + name + '.jpg', 'wb') as f:
                f.write(p.content)
            print('完成第' + name + '张')

    def find_cur_and_next_page_urls(surl):
        try:
            texts2 = me.requester_id(surl, 'i3', 'div')
        except requests.exceptions.Timeout:
            print("请求超时了呢")
        else:
            req = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             str(texts2))
            return req


    def search():
        me = main_exhentai()
        mw = main_word.get()
        nm = count.get()
        main_exhentai.search_word += mw
        if nm != '':
            me.num = int(nm)
        if int(nm) % 25 == 0:
            cirtime = int(int(nm) / 25)
        else:
            cirtime = int(int(nm) / 25) + 1
        print('共计需要' + str(cirtime) + '轮扒取')
        for i in range(0, cirtime):
            print('开始第' + str(i + 1) + '轮种子扒取')
            me.step_getpage_donurl()
            me.step_getdownloadpage()
            me.step_gettorrent()
            me.donwloader()
            main_exhentai.search_word = '?page=' + str(i + 1) + '&f_search=' + mw
            me.num -= 25


    def pic_spider():
        me = main_exhentai()
        print(me.head)
        upseturl = []
        upseturl.append(url1.get())
        # upseturl.append(url2.get())
        for i in range(0, len(upseturl)):
            if upseturl[i] != '':
                me.url = upseturl[i]
                me.get_book_info()
                me.create_download_book_dirs()
                t = threading.Thread(target=check_resumable_download, args=(me.page_num, me.surl, me.path, upseturl[i]))
                t.start()



    # 可视化内容
    tkinter.Label(tk, text="\n\n").pack()
    tkinter.Label(tk, text="\n自动下载带有标签的种子", fg='blue').pack()
    l1 = tkinter.Label(tk, text="\n以关键字搜索本子")  # 标签
    l1.pack()
    main_word = tkinter.Entry()
    main_word.pack()
    l2 = tkinter.Label(tk, text="修改回调的结果数量(建议不要太大)")  # 标签
    l2.pack()
    count = tkinter.Entry()
    count.pack()
    tkinter.Button(tk, text="开始爬！", command=search).pack()

    tkinter.Label(tk, text="\n下载模式", fg='blue').pack()
    tkinter.Label(tk, text="请给出你的页面链接(https://exhentai.org/g/xxx/xxx/)").pack()
    tkinter.Label(tk, text="如果不幸因为意外中断了，或者缺页，重新再爬一次就行，会自动找到中断点").pack()
    url1 = tkinter.Entry()
    url1.pack()
    # url2 = tkinter.Entry()
    # url2.pack()
    tkinter.Button(tk, text="开始爬图片！", command=pic_spider).pack()
    tk.mainloop()
