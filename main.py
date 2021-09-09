import tkinter.messagebox
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
        self.__pathtoowl = ''
        self.__checked_characters = list()
        self.__root = tk.Tk()
        self.__root['bg'] = 'white'
        self.__root.title('Визуализатор')
        self.__root.wm_attributes('-alpha', 0.95)
        self.__root.geometry(f'{WindowApp.WIDTH}x{WindowApp.HEIGHT}')

        self.__root.resizable(width=False, height=False)

        self.__canvas = tk.Canvas(self.__root, height=WindowApp.HEIGHT, width=WindowApp.WIDTH)
        self.__frame = tk.Frame(self.__root, bg='white')
        self.__frame.place(relwidth=1, relheight=1)

        # tk.Label(self.frame,
        #          text='1) Укажите расположение онтологии',
        #          bg='gray',
        #          font=40,
        #          padx=10,
        #          pady=10,
        #          anchor='w',
        #          justify=tk.LEFT).place(relx=, rely=)  # grid, place - расположение на frame

        self.__openBtn = tk.Button(self.__frame, text='Открыть онтологию', command=self.__select_file)
        self.__openBtn.place(relx=0.05, rely=0.05, relheight=0.11, relwidth=0.4)

        self.__create_characters()
        self.__create_charts()

        self.__deselectBtn = tk.Button(self.__frame,
                                       text='Оменить все',
                                       command=self.__callback_deselect_all)
        self.__deselectBtn.place(relx=0.05, rely=0.75)

        self.__buildBtn = tk.Button(self.__frame, text='Построить', state='disable', command=self.__callback_build_button)
        self.__buildBtn.place(relx=0.8, rely=0.85)

        self.__root.mainloop()

    def __create_characters(self):
        self.__degree = tk.BooleanVar()
        self.__degreeChBtn = tk.Checkbutton(self.__frame,
                                            text='Степени вершин',
                                            variable=self.__degree,
                                            offvalue=False,
                                            onvalue=True,
                                            command=self.__callback_degree,
                                            state=tk.DISABLED,
                                            bg='white')
        self.__degreeChBtn.place(rely=0.25, relx=0.05)

        self.__pageRank = tk.BooleanVar()
        self.__pageRankChBtn = tk.Checkbutton(self.__frame,
                                              text='Page Rank',
                                              variable=self.__pageRank,
                                              offvalue=False,
                                              onvalue=True,
                                              command=self.__callback_page_rank,
                                              state=tk.DISABLED,
                                              bg='white')
        self.__pageRankChBtn.place(rely=0.35, relx=0.05)

        self.__betweenness = tk.BooleanVar()
        self.__betweennessChBtn = tk.Checkbutton(self.__frame,
                                                 text='Степень посредничества',
                                                 variable=self.__betweenness,
                                                 offvalue=False,
                                                 onvalue=True,
                                                 command=self.__callback_betweennes,
                                                 state=tk.DISABLED,
                                                 bg='white')
        self.__betweennessChBtn.place(rely=0.45, relx=0.05)

        self.__closeness = tk.BooleanVar()
        self.__closenessChBtn = tk.Checkbutton(self.__frame,
                                               text='Степень близости',
                                               variable=self.__closeness,
                                               offvalue=False,
                                               onvalue=True,
                                               command=self.__callback_closeness,
                                               state=tk.DISABLED,
                                               bg='white')
        self.__closenessChBtn.place(rely=0.55, relx=0.05)

        self.__eigCen = tk.BooleanVar()
        self.__eigCenChBtn = tk.Checkbutton(self.__frame,
                                            text='Степень влиятельности',
                                            variable=self.__eigCen,
                                            offvalue=False,
                                            onvalue=True,
                                            command=self.__callback_eigenvector_centrality,
                                            state=tk.DISABLED,
                                            bg='white')
        self.__eigCenChBtn.place(rely=0.65, relx=0.05)

    def __create_charts(self):
        self.__chart = tk.IntVar()
        self.__lineChartRB = tk.Radiobutton(self.__frame,
                                            text='Линейный',
                                            bg='white',
                                            variable=self.__chart,
                                            value=1,
                                            state=tk.DISABLED,
                                            command=self.__check_buildBtn)
        self.__lineChartRB.place(relx=0.5, rely=0.25)

        self.__line_3dChartRB = tk.Radiobutton(self.__frame,
                                               text='Линейный 3D',
                                               bg='white',
                                               variable=self.__chart,
                                               value=2,
                                               state=tk.DISABLED,
                                               command=self.__check_buildBtn)
        self.__line_3dChartRB.place(relx=0.7, rely=0.25)

        self.__histogramChartRB = tk.Radiobutton(self.__frame,
                                                 text='Гистограмма',
                                                 bg='white',
                                                 variable=self.__chart,
                                                 value=3,
                                                 state=tk.DISABLED,
                                                 command=self.__check_buildBtn)
        self.__histogramChartRB.place(relx=0.5, rely=0.35)

        self.__ternaryChartRB = tk.Radiobutton(self.__frame,
                                               text='Ternary',
                                               bg='white',
                                               variable=self.__chart,
                                               value=4,
                                               state=tk.DISABLED,
                                               command=self.__check_buildBtn)
        self.__ternaryChartRB.place(relx=0.7, rely=0.35)

        self.__barChartRB = tk.Radiobutton(self.__frame,
                                           text='Bar',
                                           bg='white',
                                           variable=self.__chart,
                                           value=5,
                                           state=tk.DISABLED,
                                           command=self.__check_buildBtn)
        self.__barChartRB.place(relx=0.5, rely=0.45)

        self.__scatter_plotsChartRB = tk.Radiobutton(self.__frame,
                                                     text='Scatter',
                                                     bg='white',
                                                     variable=self.__chart,
                                                     value=6,
                                                     state=tk.DISABLED,
                                                     command=self.__check_buildBtn)
        self.__scatter_plotsChartRB.place(relx=0.7, rely=0.45)

        self.__scatterMatrixChartRB = tk.Radiobutton(self.__frame,
                                                     text='Scatter Matrix',
                                                     bg='white',
                                                     variable=self.__chart,
                                                     value=7,
                                                     state=tk.DISABLED,
                                                     command=self.__check_buildBtn)
        self.__scatterMatrixChartRB.place(relx=0.5, rely=0.55)

        self.__scatter_3dChartRB = tk.Radiobutton(self.__frame,
                                                  text='Scatter 3D',
                                                  bg='white',
                                                  variable=self.__chart,
                                                  value=8,
                                                  state=tk.DISABLED,
                                                  command=self.__check_buildBtn)
        self.__scatter_3dChartRB.place(relx=0.7, rely=0.55)

    def __select_file(self):
        filetypes = (
            ('OWL files', '*.owl'),
            ('All files', '*.*')
        )

        self.__pathtoowl = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        self.__chartBuild = Charts(self.__pathtoowl)

        if self.__pathtoowl != '':
            self.__degreeChBtn['state'] = tk.NORMAL
            self.__pageRankChBtn['state'] = tk.NORMAL
            self.__betweennessChBtn['state'] = tk.NORMAL
            self.__closenessChBtn['state'] = tk.NORMAL
            self.__eigCenChBtn['state'] = tk.NORMAL

    def __check_buildBtn(self):
        character = False
        plot = False
        if self.__degree.get() or self.__pageRank.get() or self.__betweenness.get() or self.__closeness.get() or self.__eigCen.get():
            character = True

        if self.__chart.get() != 0:
            plot = True

        if character and plot:
            self.__buildBtn['state'] = tk.NORMAL
        else:
            self.__buildBtn['state'] = tk.DISABLED

    def __callback_degree(self):
        if self.__degree.get():
            self.__checked_characters.append('Degree')
        else:
            self.__checked_characters.remove('Degree')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_page_rank(self):
        if self.__pageRank.get():
            self.__checked_characters.append('PageRank')
        else:
            self.__checked_characters.remove('PageRank')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_betweennes(self):
        if self.__betweenness.get():
            self.__checked_characters.append('Betweenness')
        else:
            self.__checked_characters.remove('Betweenness')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_closeness(self):
        if self.__closeness.get():
            self.__checked_characters.append('Closeness')
        else:
            self.__checked_characters.remove('Closeness')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __callback_eigenvector_centrality(self):
        if self.__eigCen.get():
            self.__checked_characters.append('Eigenvector_centrality')
        else:
            self.__checked_characters.remove('Eigenvector_centrality')
        self.__check_chart_build()
        self.__check_buildBtn()

    def __check_chart_build(self):
        self.__chart.set(0)
        for rb in [self.__lineChartRB, self.__scatterMatrixChartRB, self.__scatter_plotsChartRB, self.__scatter_3dChartRB,
                   self.__histogramChartRB, self.__barChartRB, self.__line_3dChartRB, self.__ternaryChartRB]:
            rb['state'] = tk.DISABLED
            rb['bg'] = 'white'

        if len(self.__checked_characters) == 1:
            self.__histogramChartRB['state'] = tk.NORMAL
            self.__histogramChartRB['bg'] = '#8ae36d'
            self.__barChartRB['state'] = tk.NORMAL
            self.__barChartRB['bg'] = '#8ae36d'
            self.__lineChartRB['state'] = tk.NORMAL
            self.__lineChartRB['bg'] = '#8ae36d'
        elif len(self.__checked_characters) == 2:
            self.__barChartRB['state'] = tk.NORMAL
            self.__barChartRB['bg'] = '#8ae36d'
            self.__scatter_plotsChartRB['state'] = tk.NORMAL
            self.__scatter_plotsChartRB['bg'] = '#8ae36d'
            self.__lineChartRB['state'] = tk.NORMAL
            self.__lineChartRB['bg'] = '#8ae36d'
            self.__scatterMatrixChartRB['state'] = tk.NORMAL
            self.__scatterMatrixChartRB['bg'] = '#8ae36d'
        elif len(self.__checked_characters) == 3:
            self.__scatter_plotsChartRB['state'] = tk.NORMAL
            self.__scatter_plotsChartRB['bg'] = '#8ae36d'
            self.__scatter_3dChartRB['state'] = tk.NORMAL
            self.__scatter_3dChartRB['bg'] = '#8ae36d'
            self.__line_3dChartRB['state'] = tk.NORMAL
            self.__line_3dChartRB['bg'] = '#8ae36d'
            self.__ternaryChartRB['state'] = tk.NORMAL
            self.__ternaryChartRB['bg'] = '#8ae36d'
            self.__scatterMatrixChartRB['state'] = tk.NORMAL
            self.__scatterMatrixChartRB['bg'] = '#8ae36d'
        elif len(self.__checked_characters) == 4:
            self.__scatter_plotsChartRB['state'] = tk.NORMAL
            self.__scatter_plotsChartRB['bg'] = '#8ae36d'
            self.__scatter_3dChartRB['state'] = tk.NORMAL
            self.__scatter_3dChartRB['bg'] = '#8ae36d'
            self.__ternaryChartRB['state'] = tk.NORMAL
            self.__ternaryChartRB['bg'] = '#8ae36d'
            self.__scatterMatrixChartRB['state'] = tk.NORMAL
            self.__scatterMatrixChartRB['bg'] = '#8ae36d'
        elif len(self.__checked_characters) == 5:
            self.__scatter_3dChartRB['state'] = tk.NORMAL
            self.__scatter_3dChartRB['bg'] = '#8ae36d'
            self.__ternaryChartRB['state'] = tk.NORMAL
            self.__ternaryChartRB['bg'] = '#8ae36d'
            self.__scatterMatrixChartRB['state'] = tk.NORMAL
            self.__scatterMatrixChartRB['bg'] = '#8ae36d'

    def __callback_deselect_all(self):
        for check in [self.__degreeChBtn, self.__pageRankChBtn, self.__betweennessChBtn, self.__closenessChBtn, self.__eigCenChBtn]:
            check.deselect()

    def __callback_build_button(self):
        try:
            if self.__chart.get() == 1:
                self.__chartBuild.line(self.__checked_characters)
            elif self.__chart.get() == 2:
                self.__chartBuild.line_3d(self.__checked_characters)
            elif self.__chart.get() == 3:
                self.__chartBuild.histogram(self.__checked_characters)
            elif self.__chart.get() == 4:
                self.__chartBuild.ternary(self.__checked_characters)
            elif self.__chart.get() == 5:
                self.__chartBuild.bar(self.__checked_characters)
            elif self.__chart.get() == 6:
                self.__chartBuild.scatter_plots(self.__checked_characters)
            elif self.__chart.get() == 7:
                self.__chartBuild.scatter_matrix(self.__checked_characters)
            elif self.__chart.get() == 8:
                self.__chartBuild.scatter_3d(self.__checked_characters)
        except ValueError:
            tkinter.messagebox.showerror(title='Ошибка',
                                         message='Что-то пошло не так =( Попробуйте изменить порядок выбранных характеристик и попробуйте снова.')


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
# # print(df['Closeness'].min())
#
# fig = px.scatter_matrix(df, dimensions=["Degree", "Eigenvector_centrality", "Betweenness", "Closeness"],
#                         color="Class", hover_name="Name")
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
