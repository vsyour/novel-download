#encoding=utf-8
import sys,random
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui import *
import re
import os
import socket
import time
import urllib.request
my_headers = [
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
]
def open_post(url,data):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', random.choice(my_headers))
    data = data.encode('utf-8')
    request = urllib.request.urlopen(req,data)

    return request
def search(self):
    data = self.text

    url ='http://www.lanseshuba.com/modules/article/search.php'
    print(self.xs_search)
    if self.xs_search:
        data = urllib.parse.urlencode({
            'searchtype':'articlename',
            'searchkey':data.encode('gbk')
            })
    else:
        data = urllib.parse.urlencode({
            'searchtype':'author',
            'searchkey':data.encode('gbk')
            })
    content = open_post(url,data).read().decode('gbk')
    zz = r'<td class="odd"><a href="(.*?)">(.*?)</a></td>.*?target="_blank">(.*?)</a>.*?<td class="odd">(.*?)</td>'
    zz = re.compile(zz,re.S)
    result = re.findall(zz,content)
    return result
def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', random.choice(my_headers))
    respond = urllib.request.urlopen(req)
    respond = respond.read()
    return respond

def pipei(respond,zz):
    result = re.findall(zz,respond)
    return result
# socket.setdefaulttimeout(3)

# 打开浏览器固定网页
# webbrowser.open('http://www.lanseshuba.com/', new=0, autoraise=True) 

def download(self, page):
    try:
        url2 = self.url2
        # request2 = open0.open0(url2)

        request2 = open_url(url2).decode('gbk')
        zz = re.compile(r'<dd id="contents">(.*?)</dd>',re.S)
        content_list = pipei(request2,zz)[0]
        # while '&nbsp;&nbsp;&nbsp;&nbsp;' in content_list:

        content_list = content_list.replace('&nbsp;&nbsp;&nbsp;&nbsp;','    ')
        content_list = content_list.replace('<br />','')
        # content_list = content_list.replace('\n','')
        f = self.f

        f.write(content_list + '\n\n\n\n\n\n')
        f.close()
        self.wenben =  page[1] + '\t' + "下载完成！"
        self.now = self.pagelist.index(page)
        self.genxin.emit(self.all,self.now,self.wenben,self.biaoti)
        if self.now + 1 == len(self.pagelist):
            self.finish = True
    except Exception as e:      
        print(e)
        download(self, page)

class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

        self.workThread = WorkThread()
        self.workThread.genxin.connect(self.gengxin)

        self.workcheck = Workcheck()   
        self.workcheck.well.connect(self.well) 

        self.worksearch = Worksearch()
        self.worksearch.well.connect(self.search_well)
        self.worksearch.stop_error.connect(self.stop_error)

        self.listWidget_2.itemClicked.connect(self.check)
        self.i = 0
        # self.a = ''
        self.timer = QTimer(self)
        self.wait_str = '加载中(∩_∩)'
        self.timer.timeout.connect(self.load)
        # self.timer.timeout.connect(self.slot2)
        self.pushButton.setEnabled(False)
        self.radioButton.setChecked(True)
     

        self.worksearch.xs_search = True
   

    def work(self):
        # self.timer.start(100)
        self.workThread.url = self.url
        self.workThread.start()
        self.pushButton.setEnabled(False)
        

        
    def slot2(self):
  
        self.lineEdit.setCursorPosition(1)

    def stop_error(self):
        # self.workThread.quit()
        self.timer.stop()
        self.label_4.setText('')
        if self.worksearch.xs_search:
            QMessageBox.about(self,'提示','(*>﹏<*)没有找到小说：'+ self.lineEdit_2.text())
        else:
            QMessageBox.about(self,'提示','(*>﹏<*)没有找到作者：'+ self.lineEdit_2.text())
        self.lineEdit_2.setText('')
        self.pushButton.setEnabled(False)
   
    def gengxin(self,all,now,wenben,biaoti):
        self.listWidget.insertItem(0,wenben)
        self.label_3.setText(biaoti + '(' + str(now+1) + '/' + str(all) + ')')
        self.progressBar.setValue((now+1)/all*100)
        if self.workThread.finish:
            self.workThread.finish = False
            QMessageBox.about(self,'提示','下载完成！')
            self.pushButton.setEnabled(False)
            
    def check(self,index):
        self.timer.start(100)
        self.workcheck.url = 'http://www.lanseshuba.com' + self.worksearch.xiaoshuo[self.listWidget_2.currentRow()][0]
        self.workcheck.start()
        print(self.workcheck.url)
        # self.workThread.finished.connect(self.stop_error)
    def well(self,biaoti,all):
        self.timer.stop()
        self.label_4.setText('')
        self.url = self.workcheck.url
        self.label_3.setText(biaoti + '(0/' + str(all) + ')')
        self.progressBar.setValue(0)
        self.pushButton.setEnabled(True)

    def search(self):
        if self.lineEdit_2.text() == '':
            QMessageBox.about(self,'提示','(*>﹏<*)不输入内容人家怎么搜嘛！')
        else:
            self.listWidget_2.clear()
            self.worksearch.text = self.lineEdit_2.text()
            self.worksearch.start()
            self.timer.start(100)
    def search_well(self,xiaoshuo):
        self.timer.stop()
        self.label_4.setText('')
        xiao_list = [i[1]+"\n作者：" + i[3] + '\t最新章节：' + i[2] for i in xiaoshuo]

        self.listWidget_2.addItems(xiao_list )
    def xs_search(self):
        self.lineEdit_2.setText('')
        self.worksearch.xs_search = True
        self.lineEdit_2.setPlaceholderText('请输入小说名')
    def zz_search(self):
        self.lineEdit_2.setText('')
        self.worksearch.xs_search = False
        self.lineEdit_2.setPlaceholderText('请输入作者名')
    def load(self):
        if self.wait_str == '加载中(∩_∩)......':
            self.wait_str = '加载中(∩_∩)'
        self.label_4.setText(self.wait_str)
        self.wait_str += '.'

class WorkThread(QThread):
    """docstring for WorkThread"""
    genxin = pyqtSignal(int,int,str,str)
    
    def __init__(self):
        super(WorkThread, self).__init__()
    def run(self):
        self.finish = False
        self.wenben = ''
        self.now = 0

        try:
            request = open_url(self.url).decode('gbk')
        except Exception as e:
            print('地址错误！')




        pagelist = pipei(request,r'<td class="L"><a href="(.*?)">(.*?)</a>')

        self.biaoti = pipei(request,r'<h1>(.*?)</h1>')[0]

        self.pagelist = pagelist

        self.all = len(pagelist)

        if os.path.isfile(self.biaoti + '.txt'): 
            f = open(self.biaoti + '.txt', "r", encoding='utf-8')
            download_content = f.read()
            f.close()
            for page in pagelist:             
       
                if download_content.find(page[1]) != -1:
                    self.wenben = page[1] + '\t' + '已经下载过了'

                    self.now = self.pagelist.index(page)
                    self.genxin.emit(self.all,self.now,self.wenben,self.biaoti)
                    self.wait()
                    if self.now + 1 == len(self.pagelist):
                        self.finish = True
                else:
                    f = open(self.biaoti + '.txt', "a", encoding='utf-8')
                    self.f = f
                    f.write( page[1] + '\n\n\n')
                    url2 = self.url.replace('index.html',page[0])
                    self.url2 = url2
                    download(self, page)
        else:
            for page in pagelist:
                f = open(self.biaoti + '.txt', "a", encoding='utf-8')
                self.f = f
                f.write(page[1] + '\n\n\n')
                url2 = self.url.replace('index.html',page[0])
                self.url2 = url2
                download(self, page)



class Workcheck(QThread):
    """docstring for WorkThread"""
    
    well = pyqtSignal(str,int)
    def __init__(self):
        super(Workcheck, self).__init__()
    def run(self):
        try:
            # print(self.currentThreadId())
            request = open_url(self.url).decode('gbk')
            pagelist = pipei(request,r'<td class="L"><a href="(.*?)">(.*?)</a>')

            self.biaoti = pipei(request,r'<h1>(.*?)</h1>')[0]

            print(self.biaoti)
            self.all = len(pagelist)
            self.well.emit(self.biaoti,self.all)
            self.wait()

        except Exception as e:
            print(e)
            self.wait()

class Worksearch(QThread):
    """docstring for WorkThread"""
    well = pyqtSignal(list)
    stop_error = pyqtSignal()
    def __init__(self):
        super(Worksearch, self).__init__()
    def run(self):
        try:
            self.xiaoshuo = search(self)
            if self.xiaoshuo == []:
                self.stop_error.emit()
                self.wait()
            else:
                self.well.emit(self.xiaoshuo)


        except Exception as e:
            print(e)
            
if __name__=='__main__':
    app = QApplication(sys.argv)
    mywin = MyMainWindow()
    # mywin =QWidget()



    mywin.show()
    sys.exit(app.exec_())
