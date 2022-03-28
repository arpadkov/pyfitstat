from pyfitstat.gui.GUIInfoboxWidget import ListSummaryInfobox, ActivityInfobox
from pyfitstat.model.project_model import ViewType, ActivityInfo

from PyQt5 import QtWidgets, QtCore

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
import gc


class PlotWidget(QtWidgets.QWidget):

    plot_clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.parent = parent

        self.setMinimumSize(1200, 500)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.canvas.mpl_connect('pick_event', self.artist_clicked)
        self.figure.canvas.mpl_connect('motion_notify_event', self.mouse_motion)
        # self.figure.canvas.mpl_connect('figure_enter_event', self.parent.show_popup)
        self.figure.canvas.mpl_connect('figure_leave_event', self.mouse_left)

        # self.setMouseTracking(True)
        # self.positionChanged.connect(self.cursor_changed)

        self.bars = []
        self.vlines = []
        self.ax = None
        self.annotations = []
        # self.states = []

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        # self.setBaseSize(1200, 800)

    def plot(self):
        if self.parent.model:
            self._on_plot()

    def _on_plot(self):

        gc.collect()

        plot_data = self.parent.model.plot_data

        plt.ion()

        self.figure.clear()
        self.bars = []
        self.vlines = []
        self.ax = None
        self.annotations = []

        self.ax = self.figure.add_subplot(111)

        if hasattr(plot_data, 'values'):

            if plot_data.view_type == ViewType.Month:
                self.ax.set_xticks([x for x in plot_data.labels])

            for i in range(len(plot_data.values)):

                self.vlines.append(plt.axvline(
                    plot_data.labels[i],
                    color='k',
                    linestyle='--',
                    visible=False,
                    zorder=0
                ))

                self.bars.append(self.ax.bar(
                    plot_data.labels[i],
                    plot_data.values[i],
                    gid=i,
                    picker=1,
                    color='royalblue',
                    zorder=1
                ))

                self.create_annotation(summary=plot_data.summaries[i], num=i)

        if hasattr(plot_data, 'y_label'):
            self.ax.set_ylabel(plot_data.y_label, loc='top', rotation=0)

        plt.title(plot_data.title)

        self.canvas.draw()

        self.move_annotations()

    def create_annotation(self, summary, num):

        view_type = self.parent.model.view_type
        act_info = self.parent.model.act_info

        if view_type == ViewType.Month:
             annot = ActivityInfobox(activity=summary)

            # self.annotations.append(annot)
            # return

        else:

            annot = ListSummaryInfobox(summary)

        # if act_info == ActivityInfo.Distance:
        #     value = summary.distance
        #     annot = DistanceInfobox(value=value, parent=self)
        #
        # if act_info == ActivityInfo.ElevationGain or act_info == ActivityInfo.ElevationLoss:
        #     annot = ElevationInfobox()
        #
        # if act_info == ActivityInfo.Duration:
        #     annot = DurationInfobox()

        self.annotations.append(annot)

    def move_annotations(self):

        for annot in self.annotations:      # widgets must be shown first to finalize position
            annot.set_state(True)
            annot.set_state(False)

        num = 0
        for annot, bar in zip(self.annotations, self.bars):
            self.move_annotation(annot, bar, num)
            num += 1

    def move_annotation(self, annot, bar, num):

        # coords of center of rectangle in axes
        rect_xy = self.bars[num].patches[0].get_xy()
        rect_center_x_ax = rect_xy[0] + self.bars[num].patches[0].get_width() / 2
        rect_center_y_ax = rect_xy[1] + self.bars[num].patches[0].get_height() / 2

        # center of rectangle in canvas
        rect_center_x_canv = self.transform_fig_to_ax_x(rect_center_x_ax)
        rect_center_y_canv = self.transform_fig_to_ax_y(rect_center_y_ax)

        # center of rectangle in desktop in pixels
        center_x_pix = self.transform_ax_to_pix_x(rect_center_x_canv)
        center_y_pix = self.transform_ax_to_pix_y(rect_center_y_canv)

        # plot_center_y_ax = 0.5
        plot_center_y_canv = 0.8
        plot_center_y_pix = self.transform_ax_to_pix_y(plot_center_y_canv)

        annot_width = annot.size().width()

        annot.move(center_x_pix - annot_width/2, plot_center_y_pix)

    @property
    def canvas_top_left(self):
        return self.canvas.mapToGlobal(QtCore.QPoint(0, 0))

    @property
    def fig_bbox(self):
        return self.ax.get_position()

    def transform_ax_to_pix_x(self, x):
        return self.canvas.size().width() * x + self.canvas_top_left.x()

    def transform_ax_to_pix_y(self, y):
        return self.canvas.size().height() * (1 - y) + self.canvas_top_left.y()

    def transform_fig_to_ax_x(self, x):

        coord_delta = x - self.ax.get_xlim()[0]
        ax_length = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])

        # coords in ax as fraction of axis length
        bar_coord_in_ax = coord_delta / ax_length

        # length of axes as in figure length
        ax_length = self.fig_bbox.x1 - self.fig_bbox.x0

        return self.fig_bbox.x0 + bar_coord_in_ax * ax_length

    def transform_fig_to_ax_y(self, y):

        coord_delta = y - self.ax.get_ylim()[0]
        ax_length = (self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

        # coords in ax as fraction of axis length
        bar_coord_in_ax = coord_delta / ax_length

        # length of axes as in figure length
        ax_length = self.fig_bbox.y1 - self.fig_bbox.y0

        return self.fig_bbox.y0 + bar_coord_in_ax * ax_length

    def artist_clicked(self, event):
        if self.parent.model.view_type is not ViewType.Month:
            for annot in self.annotations:
                annot.deleteLater()

        self.plot_clicked.emit(event.artist.get_gid())

    def mouse_motion(self, event):

        if event.inaxes == self.ax:

            for bar, annot, vline in zip(self.bars, self.annotations, self.vlines):
                cont, ind = bar.patches[0].contains(event)

                if cont:
                    annot.set_state(True)
                    vline.set_visible(True)

                else:
                    annot.set_state(False)
                    vline.set_visible(False)

    def mouse_left(self, event):
        for annot, vline in zip(self.annotations, self.vlines):
            annot.hide()
            vline.set_visible(False)
