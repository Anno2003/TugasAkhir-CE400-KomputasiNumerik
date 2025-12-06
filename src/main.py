import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import numpy as np

import roots
import linear
import interpolasi
import integral
import regression
import differentiation

plt.rcParams["axes.grid"] = True # supaya defaultnya ada grid

class KOMNUMApp:
    def __roots_page(self):
        return ft.Container(content=
            ft.Column(
                [
                    ft.TextField(label="f(x)="),
                    ft.TextField(label="start"),
                    ft.TextField(label="end"),
                    ft.Dropdown(
                        options=[
                            ft.DropdownOption(key="Bisection"),
                            ft.DropdownOption(key="Regula-falsi"),
                            ft.DropdownOption(key="Newton-raphson"),
                            ft.DropdownOption(key="Secant")
                        ]
                    ),
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK)
                ]
            ),
            alignment=ft.alignment.center
        )

    def __linear_page(self): 
        return ft.Container(content=
            ft.Text("test2"),
            alignment=ft.alignment.center
        )

    def __interpolasi_page(self):
        return ft.Container(content=
            ft.Text("test3"),
            alignment=ft.alignment.center
        )

    def __integral_page(self):
        return ft.Container(content=
            ft.Column(
                [
                    ft.TextField(label="f(x)="),
                    ft.ResponsiveRow(
                        [
                            ft.TextField(col={"sm":3},label="a="),
                            ft.TextField(col={"sm":3},label="b="),
                            ft.TextField(col={"sm":3},label="n=")
                        ],
                    ),
                    ft.Dropdown(
                        options=[
                            ft.DropdownOption(key="Trapezoid"),
                            ft.DropdownOption(key="Simpson 1/3"),
                            ft.DropdownOption(key="Simpson 3/8"),
                        ]
                    ),
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK)
                ],
                expand=1
            ),
            alignment=ft.alignment.center
        )

    def __regresi_page(self):
        x = ft.TextField(label="x=")
        y = ft.TextField(label="y=")
        fig,ax = plt.subplots()
        
        def calc(e):
            _x=[float(i.strip())for i in x.value.split(',')]
            _y=[float(i.strip())for i in y.value.split(',')]
            a,b=regression.linear_regression(_x,_y)
            f = lambda x: a+b*x
            
            _x
            Y= [f(i) for i in _x]
            ax.clear()
            ax.set_title(f"f(x)={round(a,4)}+{round(b,4)}x")
            ax.scatter(_x,_y,color='red')
            ax.plot(_x,Y)
            self.page.update()
            
        return ft.Container(content=
            ft.Column(
                [
                    ft.Text("x dan y dalam comma separated values 1,2,3,..."),
                    x,
                    y,
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK,on_click=calc),
                    MatplotlibChart(fig,expand=1)
                ],
                expand=1
            ),
            alignment=ft.alignment.center
        )

    def __differential_page(self):
        return ft.Container(content=
            ft.Column(
                [
                    ft.TextField(label="f(x,y)="),
                    ft.ResponsiveRow(
                        [
                            ft.TextField(col={"sm":3},label="x0="),
                            ft.TextField(col={"sm":3},label="y0="),
                            ft.TextField(col={"sm":3},label="b="),
                            ft.TextField(col={"sm":3},label="h=")
                        ],
                    ),
                    ft.Dropdown(
                        options=[
                            ft.DropdownOption(key="Euler"),
                            ft.DropdownOption(key="Heun"),
                        ]
                    ),
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK)
                ],
                expand=1
            ),
            alignment=ft.alignment.center
        )

    def __init__(self,page:ft.Page):
        self.page = page
        self.page.title = "Tugas Rancang Komputasi Numerik"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.resizable = True
        self.create_ui_components()

        self.page.update()
        pass

    def create_ui_components(self):
        title = ft.Column(
            controls=[
                ft.Text("Tugas Rancang Komnum",theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Text("Daya Sjahpoetro 622022003",theme_style=ft.TextThemeStyle.TITLE_SMALL)
            ]
        )
        tabs =ft.Tabs(
            selected_index = 0,
            animation_duration = 300,
            tabs=[
                ft.Tab(text = "Roots", content = self.__roots_page()),
                ft.Tab(text = "Persamaan Linear",content = self.__linear_page()),
                ft.Tab(text = "Interpolasi",content = self.__interpolasi_page()),
                ft.Tab(text = "Integral",content = self.__integral_page()),
                ft.Tab(text = "Regresi",content= self.__regresi_page()),
                ft.Tab(text = "Persamaan Differensial",content=self.__differential_page())
            ],
            expand = 1,
        )
        self.page.add(title)
        self.page.add(tabs)
        pass


def main(page: ft.Page):
    app = KOMNUMApp(page)

if __name__=="__main__":
    ft.app(target=main)