# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os, random
import numpy as np
from PyQt4 import QtGui, QtCore, uic
from ui_tickviewer import Ui_MainWindow


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

l = 200
tmp = np.cumsum(np.random.randint(-1,2,l))
bidprice = tmp * 0.2 + 2233
askprice = bidprice + 0.2
tmp = np.random.randint(0,2,l)
price = np.where(tmp==0,bidprice,askprice)



class TvWindow(QtGui.QMainWindow):
    def __init__(self):
        super(TvWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        ax = self.ui.mplcanvas.axes
        ax.hold(True)
        ax.yaxis.tick_right()
        
        
        self.setWindowTitle("Tick Viewer (%s)" % progname)
        
        self._offset = 0;
        self.drawtick()
        self.statusBar().showMessage("ready")
        
        self.showMaximized()


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self._offset += 1
            self.draw_canvas()
        if event.key() == QtCore.Qt.Key_Left:
            self._offset -= 1
            self.draw_canvas()
    
    def drawtick(self):
        mpl = self.ui.mplcanvas
        ax = mpl.axes
        
        i_start = 0
        i_end = 20
        
        ind = np.arange(i_start,i_end)
        ax.plot(bidprice[ind],'ro')
        ax.plot(askprice[ind],'go')
        
        locs = ax.yaxis.get_ticklocs()
        ax.yaxis.set_ticklabels(map(lambda x: "%.1f" % x, locs))
        
        mpl.draw()
        
    
    def draw_canvas(self):        
        mpl = self.ui.mplcanvas
        ax = mpl.axes
        
        t = np.arange(0.0 + self._offset/10., 1.6 + self._offset/10., 0.01)
        s = np.sin(2*np.pi*t)
        ax.plot(t,s)
        ax.set_xlim(0.0 + self._offset/10., 1.6 + self._offset/10.)
        mpl.draw()
        
        
    


def main():    
    app = QtGui.QApplication(sys.argv)
    tv = TvWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()