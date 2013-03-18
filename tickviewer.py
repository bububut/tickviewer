# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os, random
import numpy as np
import pandas as pd

from PyQt4 import QtGui, QtCore, uic
from ui_tickviewer import Ui_MainWindow
import matplotlib.gridspec as gridspec


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

l = 200
tmp = np.cumsum(np.random.randint(-1,2,l))
bidprice = tmp * 0.2 + 2233
askprice = bidprice + 0.2
tmp = np.random.randint(0,2,l)
price = np.where(tmp==0,bidprice,askprice)



class TvWindow(QtGui.QMainWindow):
    def _loaddata(self):
        self._data = pd.read_csv('IF1304.csv', names=['date', 'time', 'price', 'volume', 'openint', 'bid', 'bidv', 'ask', 'askv'])
        self._datalen = self._data['price'].count()


    def __init__(self):
        super(TvWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        fig = self.ui.mplcanvas.figure
        fig.delaxes(self.ui.mplcanvas.axes)
        # fig.subplots_adjust(left=0.01, right=0.96, top=0.99, bottom=0.03)
        gs = gridspec.GridSpec(2, 1, hspace = 0.01, height_ratios=[7,3])
        self._ax1 = fig.add_subplot(gs[0])
        self._ax2 = fig.add_subplot(gs[1])
        self._ax1.hold(True)
        self._ax1.yaxis.tick_right()
        self._ax2.hold(True)
        self._ax2.yaxis.tick_right()
        # ax = self.ui.mplcanvas.axes
        # ax.hold(True)
        # ax.yaxis.tick_right()
        
        self.setWindowTitle("Tick Viewer (%s)" % progname)
        
        self._loaddata()
        self._drawStart = 0;
        self._drawEnd = 100;
        self.drawtick()

        self.statusBar().showMessage("ready")
        self.showMaximized()


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            if self._drawEnd + 1 < self._datalen:
                self._drawStart += 1
                self._drawEnd += 1
            self.drawtick()
        if event.key() == QtCore.Qt.Key_Left:
            if self._drawStart - 1 >= 0:
                self._drawStart -= 1
                self._drawEnd -= 1
            self.drawtick()
    
    def drawtick(self):
        drawlen = self._drawEnd - self._drawStart
        td = self._data.iloc[self._drawStart:self._drawEnd]
        xlabel = td['time'].values

        mpl = self.ui.mplcanvas


        # tick chart
        ax = self._ax1
        ax.clear()

        ax.plot(td['price'], marker='.', lw=0.5)
        # ind = np.arange(i_start,i_end)
        # ax.plot(bidprice[ind],'ro')
        # ax.plot(askprice[ind],'go')
        ax.xaxis.set_ticklabels([])
        locs = ax.yaxis.get_ticklocs()
        ax.yaxis.set_ticklabels(map(lambda x: "%.1f" % x, locs))
        


        # volume chart
        ax = self._ax2
        ax.clear()

        ax.bar(xrange(drawlen), td['volume'],width=0.1)
        # ax.xaxis.set_ticklabels(xlabel)

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