from pyfitstat.gui.GUIInfoboxWidget import DistanceInfobox, ElevationInfobox, DurationInfobox, ActivityInfobox
from pyfitstat.model.project_model import ViewType, ActivityInfo

from PyQt5 import QtWidgets, QtCore

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PlotWidget(QtWidgets.QWidget):

    plot_clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.parent = parent

        self.setMinimumSize(800, 500)

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
        self.states = []

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def plot(self):

        plot_data = self.parent.model.plot_data

        plt.ion()

        self.figure.clear()
        self.bars = []
        self.vlines = []
        self.ax = None

        self.ax = self.figure.add_subplot(111)

        if hasattr(plot_data, 'values'):
            for i in range(len(plot_data.values)):
                self.bars.append(self.ax.bar(
                    plot_data.labels[i],
                    plot_data.values[i],
                    gid=i,
                    picker=1,
                    color='royalblue'
                ))

                self.vlines.append(plt.axvline(
                    plot_data.labels[i],
                    color='k',
                    linestyle='--',
                    visible=False
                ))




                self.create_annotation(value=plot_data.values[i], num=i)



        # i = 0
        # for annot in self.annotations:
        #
        #     i += 1

        plt.title(plot_data.title)

        self.canvas.draw()

        # self.setFixedSize(500, 500)

        self.move_annotations()

        # print(self.mapToGlobal(self.pos()))

    def create_annotation(self, value, num):

        view_type = self.parent.model.view_type
        act_info = self.parent.model.act_info

        annot = None

        if view_type == ViewType.Month:
            annot = ActivityInfobox()
            self.annotations.append(annot)
            return

        if act_info == ActivityInfo.Distance:
            annot = DistanceInfobox(value=value, parent=self)

        if act_info == ActivityInfo.ElevationGain or act_info == ActivityInfo.ElevationLoss:
            annot = ElevationInfobox()

        if act_info == ActivityInfo.Duration:
            annot = DurationInfobox()

        self.annotations.append(annot)

    def move_annotations(self):

        print(f'plot_top_left: {self.canvas.mapToGlobal(QtCore.QPoint(0, 0))}')
        # print(f'plot_size: {self.size()}')

        num = 0
        for annot, bar in zip(self.annotations, self.bars):
            self.move_annotation(annot, bar, num)
            num += 1

    """
    def move_annotation(self, annot, bar, num):

        # print('=====================================')
        # print(f'Annotation - {num}')

        plot_top_left = self.canvas_top_left
        # plot_top_left = self.parent.plot_widget_pos()
        plot_size = self.size()

        # print(f'Size of plot:              x = {plot_size.width()} y = {plot_size.height()}')

        # print(f'Plot top left pixel:       x = {plot_top_left.x()} y = {plot_top_left.y()}')

        # print(f'Axes position in figure    {self.ax.get_position()}')
        X = self.ax.get_position()

        # print(f'Bar position in axes       {self.bars[num].patches[0]}')



        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # xy_pixels = self.ax.transAxes.transform((3, 1000))
        # print(xy_pixels)

        # y1 =
        # y_in_axes = (y1 - y0) / 2

        # size of axes of plot in pixels
        d_ax_x_pix = self.ax.get_position().width * plot_size.width()
        d_ax_y_pix = self.ax.get_position().height * plot_size.height()

        # coords of center of rectangle in axes
        rect_xy = self.bars[num].patches[0].get_xy()
        rect_center_x = rect_xy[0] + self.bars[num].patches[0].get_width() / 2
        rect_center_y = rect_xy[1] + self.bars[num].patches[0].get_height() / 2

        # center of rectangle in axes in pixels
        rect_center_x_pix_in_ax = (rect_center_x-xlim[0]) * d_ax_x_pix / (xlim[1] - xlim[0])
        rect_center_y_pix_in_ax = (rect_center_y - ylim[0]) * d_ax_y_pix / (ylim[1] - ylim[0])

        # center of rectangle in plot in pixels#
        rect_center_x_pix_in_plot = rect_center_x_pix_in_ax + (plot_size.width() - d_ax_x_pix) / 2
        rect_center_y_pix_in_plot = rect_center_y_pix_in_ax + (plot_size.height() - d_ax_y_pix) / 2

        # center of rectangle in desktop in pixels
        rect_center_x_pix = rect_center_x_pix_in_plot + plot_top_left.x()
        rect_center_y_pix = rect_center_y_pix_in_plot + plot_top_left.y()

        # vertical center of plot
        plot_center_pix = plot_size.height()/2
        annot_y = plot_center_pix + plot_top_left.y()

        annot.move(rect_center_x_pix, annot_y)
    """

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
        plot_center_y_canv = 0.5
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
        self.plot_clicked.emit(event.artist.get_gid())

    def mouse_motion(self, event):

        # self.vlines[-1].set_visible(True)

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
        for annot in self.annotations:
            annot.hide()
