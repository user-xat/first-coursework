from owlread import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


# data = OwlRead.read_owl_file('social-model-biggest.owl')
# graph = Graph.create_graph_from_onto(data)
# print(graph.vcount())
# print(graph.ecount())
# temp = graph.vs['name']
# print('PageRank', graph.pagerank())
# # print('Degree Distribution', graph.degree_distribution())
# print('Степень влиятельности', graph.eigenvector_centrality())
# print('Степень близости', graph.closeness())
# print('Степень посредничества', graph.betweenness())
# print('Degree', graph.degree())
# print('Diameter', graph.diameter())
# print('Radius', graph.radius())
# print(graph)
# temp = graph.degree()
# temp = np.array(temp)
# histo = go.Histogram(x=temp)
# fig = go.Figure(data=[histo])


class WindowApp:
    HEIGHT = 350
    WIDTH = 500

    def __init__(self):
        self.pathtoowl = ''
        self.checked_characters = list()
        self.root = tk.Tk()
        # self.root.iconphoto(False, tk.PhotoImage(file='owl.png'))
        self.root['bg'] = 'white'
        self.root.title('Визуализатор')
        self.root.wm_attributes('-alpha', 0.95)
        self.root.geometry(f'{WindowApp.WIDTH}x{WindowApp.HEIGHT}')

        self.root.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self.root, height=WindowApp.HEIGHT, width=WindowApp.WIDTH)
        self.frame = tk.Frame(self.root, bg='white')
        self.frame.place(relwidth=1, relheight=1)

        # tk.Label(self.frame,
        #          text='1) Укажите расположение онтологии',
        #          bg='gray',
        #          font=40,
        #          padx=10,
        #          pady=10,
        #          anchor='w',
        #          justify=tk.LEFT).place(relx=, rely=)  # grid, place - расположение на frame

        self.openBtn = tk.Button(self.frame, text='Открыть онтологию', command=self.__select_file)
        self.openBtn.place(relx=0.05, rely=0.05, relheight=0.11, relwidth=0.4)

        # self.combo = ttk.Combobox(self.frame, values=WindowApp.CHARACTERISTICS, state='disable')
        # self.combo.current(0)
        # self.combo.place(relx=0.05, rely=0.25, relheight=0.11, relwidth=0.4)

        self.__create_characters()
        self.__create_charts()

        # command=some_function - функция при нажатии на кнопку
        self.buildBtn = tk.Button(self.frame, text='Построить', state='disable', command=self.__callback_build_button)
        self.buildBtn.place(relx=0.8, rely=0.85)

        self.root.mainloop()

    def __create_characters(self):
        self.degree = tk.BooleanVar()
        self.degreeChBtn = tk.Checkbutton(self.frame,
                                          text='Степени вершин',
                                          variable=self.degree,
                                          offvalue=False,
                                          onvalue=True,
                                          command=self.__callback_degree,
                                          state=tk.DISABLED,
                                          bg='white')
        self.degreeChBtn.place(rely=0.25, relx=0.05)

        self.pageRank = tk.BooleanVar()
        self.pageRankChBtn = tk.Checkbutton(self.frame,
                                            text='Page Rank',
                                            variable=self.pageRank,
                                            offvalue=False,
                                            onvalue=True,
                                            command=self.__callback_page_rank,
                                            state=tk.DISABLED,
                                            bg='white')
        self.pageRankChBtn.place(rely=0.35, relx=0.05)

        self.betweenness = tk.BooleanVar()
        self.betweennessChBtn = tk.Checkbutton(self.frame,
                                               text='Степень посредничества',
                                               variable=self.betweenness,
                                               offvalue=False,
                                               onvalue=True,
                                               command=self.__callback_betweennes,
                                               state=tk.DISABLED,
                                               bg='white')
        self.betweennessChBtn.place(rely=0.45, relx=0.05)

        self.closeness = tk.BooleanVar()
        self.closenessChBtn = tk.Checkbutton(self.frame,
                                             text='Степень близости',
                                             variable=self.closeness,
                                             offvalue=False,
                                             onvalue=True,
                                             command=self.__callback_closeness,
                                             state=tk.DISABLED,
                                             bg='white')
        self.closenessChBtn.place(rely=0.55, relx=0.05)

        self.eigCen = tk.BooleanVar()
        self.eigCenChBtn = tk.Checkbutton(self.frame,
                                          text='Степень влиятельности',
                                          variable=self.eigCen,
                                          offvalue=False,
                                          onvalue=True,
                                          command=self.__callback_eigenvector_centrality,
                                          state=tk.DISABLED,
                                          bg='white')
        self.eigCenChBtn.place(rely=0.65, relx=0.05)

    def __create_charts(self):
        self.chart = tk.IntVar()
        self.lineChartRB = tk.Radiobutton(self.frame,
                                          text='Линейный',
                                          bg='white',
                                          variable=self.chart,
                                          value=1,
                                          state=tk.DISABLED,
                                          command=self.__check_buildBtn)
        self.lineChartRB.place(relx=0.5, rely=0.25)

        self.line_3dChartRB = tk.Radiobutton(self.frame,
                                             text='Линейный 3D',
                                             bg='white',
                                             variable=self.chart,
                                             value=2,
                                             state=tk.DISABLED,
                                             command=self.__check_buildBtn)
        self.line_3dChartRB.place(relx=0.7, rely=0.25)

        self.histogramChartRB = tk.Radiobutton(self.frame,
                                               text='Гистограмма',
                                               bg='white',
                                               variable=self.chart,
                                               value=3,
                                               state=tk.DISABLED,
                                               command=self.__check_buildBtn)
        self.histogramChartRB.place(relx=0.5, rely=0.35)

        self.ternaryChartRB = tk.Radiobutton(self.frame,
                                             text='Ternary',
                                             bg='white',
                                             variable=self.chart,
                                             value=4,
                                             state=tk.DISABLED,
                                             command=self.__check_buildBtn)
        self.ternaryChartRB.place(relx=0.7, rely=0.35)

        self.barChartRB = tk.Radiobutton(self.frame,
                                         text='Bar',
                                         bg='white',
                                         variable=self.chart,
                                         value=5,
                                         state=tk.DISABLED,
                                         command=self.__check_buildBtn)
        self.barChartRB.place(relx=0.5, rely=0.45)

        self.scatter_plotsChartRB = tk.Radiobutton(self.frame,
                                                   text='Scatter',
                                                   bg='white',
                                                   variable=self.chart,
                                                   value=6,
                                                   state=tk.DISABLED,
                                                   command=self.__check_buildBtn)
        self.scatter_plotsChartRB.place(relx=0.7, rely=0.45)

        self.scatterMatrixChartRB = tk.Radiobutton(self.frame,
                                                   text='Scatter Matrix',
                                                   bg='white',
                                                   variable=self.chart,
                                                   value=7,
                                                   state=tk.DISABLED,
                                                   command=self.__check_buildBtn)
        self.scatterMatrixChartRB.place(relx=0.5, rely=0.55)

        self.scatter_3dChartRB = tk.Radiobutton(self.frame,
                                                text='Scatter 3D',
                                                bg='white',
                                                variable=self.chart,
                                                value=8,
                                                state=tk.DISABLED,
                                                command=self.__check_buildBtn)
        self.scatter_3dChartRB.place(relx=0.7, rely=0.55)

    def __select_file(self):
        filetypes = (
            ('OWL files', '*.owl'),
            ('All files', '*.*')
        )

        self.pathtoowl = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        self.chartBuild = Charts(self.pathtoowl)

        if self.pathtoowl != '':
            self.degreeChBtn['state'] = tk.NORMAL
            self.pageRankChBtn['state'] = tk.NORMAL
            self.betweennessChBtn['state'] = tk.NORMAL
            self.closenessChBtn['state'] = tk.NORMAL
            self.eigCenChBtn['state'] = tk.NORMAL

    def __check_buildBtn(self):
        character = False
        plot = False
        if self.degree.get() or self.pageRank.get() or self.betweenness.get() or self.closeness.get() or self.eigCen.get():
            character = True

        if self.chart.get() != 0:
            plot = True

        if character and plot:
            self.buildBtn['state'] = tk.NORMAL
        else:
            self.buildBtn['state'] = tk.DISABLED

    def __callback_degree(self):
        if self.degree.get():
            self.checked_characters.append('Degree')
        else:
            self.checked_characters.remove('Degree')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_page_rank(self):
        if self.pageRank.get():
            self.checked_characters.append('PageRank')
        else:
            self.checked_characters.remove('PageRank')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_betweennes(self):
        if self.betweenness.get():
            self.checked_characters.append('Betweenness')
        else:
            self.checked_characters.remove('Betweenness')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_closeness(self):
        if self.closeness.get():
            self.checked_characters.append('Closeness')
        else:
            self.checked_characters.remove('Closeness')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_eigenvector_centrality(self):
        if self.eigCen.get():
            self.checked_characters.append('Eigenvector_centrality')
        else:
            self.checked_characters.remove('Eigenvector_centrality')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __check_chart_build(self):
        self.chart.set(0)
        for rb in [self.lineChartRB, self.scatterMatrixChartRB, self.scatter_plotsChartRB, self.scatter_3dChartRB,
                   self.histogramChartRB, self.barChartRB, self.line_3dChartRB, self.ternaryChartRB]:
            rb['state'] = tk.DISABLED
            rb['bg'] = 'white'

        if len(self.checked_characters) == 1:
            self.histogramChartRB['state'] = tk.NORMAL
            self.histogramChartRB['bg'] = '#8ae36d'
            self.barChartRB['state'] = tk.NORMAL
            self.barChartRB['bg'] = '#8ae36d'
            self.lineChartRB['state'] = tk.NORMAL
            self.lineChartRB['bg'] = '#8ae36d'
        elif len(self.checked_characters) == 2:
            self.barChartRB['state'] = tk.NORMAL
            self.barChartRB['bg'] = '#8ae36d'
            self.scatter_plotsChartRB['state'] = tk.NORMAL
            self.scatter_plotsChartRB['bg'] = '#8ae36d'
            self.lineChartRB['state'] = tk.NORMAL
            self.lineChartRB['bg'] = '#8ae36d'
        elif len(self.checked_characters) == 3:
            self.scatter_plotsChartRB['state'] = tk.NORMAL
            self.scatter_plotsChartRB['bg'] = '#8ae36d'
            self.scatter_3dChartRB['state'] = tk.NORMAL
            self.scatter_3dChartRB['bg'] = '#8ae36d'
            self.line_3dChartRB['state'] = tk.NORMAL
            self.line_3dChartRB['bg'] = '#8ae36d'
            self.ternaryChartRB['state'] = tk.NORMAL
            self.ternaryChartRB['bg'] = '#8ae36d'
        elif len(self.checked_characters) == 4:
            self.scatter_plotsChartRB['state'] = tk.NORMAL
            self.scatter_plotsChartRB['bg'] = '#8ae36d'
            self.scatter_3dChartRB['state'] = tk.NORMAL
            self.scatter_3dChartRB['bg'] = '#8ae36d'
            self.ternaryChartRB['state'] = tk.NORMAL
            self.ternaryChartRB['bg'] = '#8ae36d'
        elif len(self.checked_characters) == 5:
            self.scatter_3dChartRB['state'] = tk.NORMAL
            self.scatter_3dChartRB['bg'] = '#8ae36d'
            self.ternaryChartRB['state'] = tk.NORMAL
            self.ternaryChartRB['bg'] = '#8ae36d'

    def __callback_build_button(self):
        if self.chart.get() == 1:
            self.chartBuild.line(self.checked_characters)
        elif self.chart.get() == 2:
            self.chartBuild.line_3d(self.checked_characters)
        elif self.chart.get() == 3:
            self.chartBuild.histogram(self.checked_characters)
        elif self.chart.get() == 4:
            self.chartBuild.ternary(self.checked_characters)
        elif self.chart.get() == 5:
            self.chartBuild.bar(self.checked_characters)
        elif self.chart.get() == 6:
            self.chartBuild.scatter_plots(self.checked_characters)
        elif self.chart.get() == 7:
            self.chartBuild.scatter_matrix(self.checked_characters)
        elif self.chart.get() == 8:
            self.chartBuild.scatter_3d(self.checked_characters)


app = WindowApp()

# data = OwlRead.read_owl_file('social-model-biggest.owl')
# graph = Graph.create_graph_from_onto(data)
#
# df = pd.DataFrame({
#     'Name': graph.vs['name'],
#     'Class': graph.vs['class'],
#     'Degree': graph.degree(),
#     'PageRank': graph.pagerank(),
#     'Betweenness': graph.betweenness(),
#     'Closeness': graph.closeness(),
#     'Eigenvector_centrality': graph.eigenvector_centrality()
# })
# print(df['Closeness'].min())

# fig = px.scatter_matrix(df, dimensions=["Degree", "Eigenvector_centrality", "Betweenness", "Closeness"],
#                         color="Class", hover_name = "Name")
# fig.show()

# fig = px.scatter_3d(df, x="Degree", y="PageRank", z="Eigenvector_centrality", color="Class", size="PageRank",
#                     hover_name="Name")
# fig.show()

# fig = px.scatter(df, x="PageRank", y="Eigenvector_centrality", color='Class', hover_name='Name', size='Degree')
# fig.show()

# fig = px.histogram(df, x="Degree", color="Class")
# fig.show()

# fig = px.bar(df, y='Degree', hover_name='Name', color='Class', orientation='h')
# fig.show()
