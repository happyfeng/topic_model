#coding:utf8
#将之前写的几个文件的功能都整合到ui窗口上
import wx
from download import download_acl
from pdfconvert import pdfcn
from delword import delw 
app = wx.App() 
def dl(evt):
    dlname = download_acl()	
    contents.SetValue(dlname)
def cv(evt):
    cvname =pdfcn()
    contents.SetValue(cvname)
def cw(evt):
    cwname =delw()
    contents.SetValue(cwname)
win = wx.Frame(None,title=u'功能框',size=(420,340))
downloadbt = wx.Button(win,label=u'下载',pos=(245,5),size=(80,25))
convertbt = wx.Button(win,label=u'pdf转换txt',pos=(325,5),size=(80,25))
cutwordbt = wx.Button(win,label=u'去停用词',pos=(125,5),size=(80,25))
contents = wx.TextCtrl(win,pos=(5,35),size=(400,300),style=wx.TE_MULTILINE|wx.HSCROLL)
downloadbt.Bind(wx.EVT_BUTTON,dl)
cutwordbt.Bind(wx.EVT_BUTTON,cw)
convertbt.Bind(wx.EVT_BUTTON,cv)
win.Show()
app.MainLoop()
