import flet as ft
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import numpy as np

import roots
import linear
import interpolasi
import integral
import regression
import differentiation

matplotlib.use('agg')
plt.rcParams["axes.grid"] = True # supaya defaultnya ada grid

class KOMNUMApp:
    
    # allowed names from numpy
    safe_np = {
        "np.sin": np.sin,
        "np.cos": np.cos,
        "np.tan": np.tan,
        "np.exp": np.exp,
        "np.log": np.log,
        "np.sqrt": np.sqrt,
        "np.abs": np.abs,
        "np.pi": np.pi,
        "np.e": np.e,
    }
    
    SAFE_GLOBALS = {
        "__builtins__": None,  # disable all builtins
        **safe_np,
        "np":np,
    }
    
    def make_function(self,expr: str):
        """Returns a callable f(x) from a user expression using math + numpy."""
        def f(x):
            # each call overrides x
            return eval(expr, self.SAFE_GLOBALS, {"x": x})
        return f
        
    def __roots_page(self):
        fig,ax = plt.subplots()
        fx = ft.TextField(label="f(x)=")
        start = ft.TextField(label="a atau x0")
        end = ft.TextField(label="b atau x1 atau df")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Bisection"),
                ft.DropdownOption(key="Regula-falsi"),
                ft.DropdownOption(key="Newton-raphson"),
                ft.DropdownOption(key="Secant")
            ]
        )
        
        def calc(e):
            _f=self.make_function(fx.value.strip())
            a = float(start.value.strip())
            
            if (dropdown.value == "Newton-raphson"):
                b = self.make_function(end.value.strip())
            else:
                b = float(end.value.strip())

            match (dropdown.value):
                case "Bisection":
                    c,_,conv = roots.bisection(_f,a,b) 
                    pass
                case "Regula-falsi":
                    c,_,conv = roots.regula_falsi_gacor(_f,a,b) 
                    pass
                case "Newton-raphson":
                    c,_,conv = roots.newton_raphson(_f,b,a) 
                    pass
                case "Secant":
                    c,_,conv = roots.secant(_f,a,b) 
                    pass
            
            if (dropdown.value == "Newton-raphson"):
                X = np.linspace(a-3,c+3,100)
            else:
                X = np.linspace(a,b,100)
            
            Y = _f(X)
            
            ax.clear()
            if(not conv):
                ax.set_title("Tidak Konvergen")
            else:
                ax.set_title(f"akar = {c}")
            ax.plot(X,Y)
            ax.scatter(c,_f(c),color='red')
            self.page.update()
            pass
        
        return ft.Container(content=
            ft.Column(
                [
                    ft.Text("input f(x) support numpy contoh: np.sin(x)+2\nuntuk newton raphson df merupakan turunan pertama dari f(x)"),
                    fx,
                    start,
                    end,
                    dropdown,
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK,on_click=calc),
                    MatplotlibChart(fig,expand=1)
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
        fx = ft.TextField(label="f(x)=")
        a = ft.TextField(col={"sm":3},label="a=")
        b = ft.TextField(col={"sm":3},label="b=")
        n = ft.TextField(col={"sm":3},label="n=")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Trapezoid"),
                ft.DropdownOption(key="Simpson 1/3"),
                ft.DropdownOption(key="Simpson 3/8"),
            ]
        )
        result = ft.Text("f'(x)=",theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        
        def calc(e):
            _a = float(a.value.strip())
            _b = float(b.value.strip())
            _n = int(n.value.strip())
            _f = self.make_function(fx.value.strip())
            
            match(dropdown.value):
                case "Trapezoid":
                    I = integral.trapezoidal_rule(_f,_a,_b,_n)
                    pass
                case "Simpson 1/3":
                    I = integral.simpson_one_third(_f,_a,_b,_n)
                    pass
                case "Simpson 3/8":
                    I = integral.simpson_three_eight(_f,_a,_b,_n)
                    pass
            
            result.value = f"f'(x) = {I}"
            self.page.update()
            pass
        
        return ft.Container(content=
            ft.Column(
                [
                    fx,
                    ft.ResponsiveRow(
                        [
                            a,
                            b,
                            n
                        ],
                    ),
                    dropdown,
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK,on_click=calc),
                    result,
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
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK),
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