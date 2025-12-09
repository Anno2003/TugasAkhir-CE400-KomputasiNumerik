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
    
    def error_dialog(self,msg):
        dlg = ft.AlertDialog(
            modal = True,
            title = ft.Text("Terjadi Kesalahan"),
            content = ft.Text(msg),
            alignment=ft.alignment.center,
            actions=[
                        ft.TextButton("OK", on_click=lambda e: self.page.close(dlg)),
            ],
            on_dismiss= lambda e:self.page.close(dlg)
        )
        self.page.open(dlg)
        self.page.update()
    
    def make_function(self,expr: str,xy=False):
        """Returns a callable f(x) from a user expression using math + numpy."""
        if(xy):
            def f(x,y):
                # each call overrides x
                return eval(expr, self.SAFE_GLOBALS, {"x": x,"y":y})
        else:
            def f(x):
                # each call overrides x
                return eval(expr, self.SAFE_GLOBALS, {"x": x})
        return f
        
    def __roots_page(self):
        
        fig,ax = plt.subplots()
        fx = ft.TextField(label="f(x)=",value="x**2-4")
        start = ft.TextField(label="a atau x0",value="0")
        end = ft.TextField(label="b atau x1 atau df",value="3")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Bisection"),
                ft.DropdownOption(key="Regula-falsi"),
                ft.DropdownOption(key="Newton-raphson"),
                ft.DropdownOption(key="Secant")
            ],
            value="Bisection"
        )
        
        def calc(e):
            try:
                _f=self.make_function(fx.value.strip())
                a = float(start.value.strip())
            
                if (dropdown.value == "Newton-raphson"):
                    b = self.make_function(end.value.strip())
                else:
                    b = float(end.value.strip())
            
                match (dropdown.value):
                    case "Bisection":
                        if (_f(a)*_f(b)>0):
                            self.error_dialog(f"tidak memenuhi syarat f(a)*f(b)<0")
                        else:
                            c,_,conv = roots.bisection(_f,a,b) 
                            
                    case "Regula-falsi":
                        if (_f(a)*_f(b)>0):
                            self.error_dialog(f"tidak memenuhi syarat f(a)*f(b)<0")
                        else:
                            c,_,conv = roots.regula_falsi_gacor(_f,a,b) 
                    case "Newton-raphson":
                        c,_,conv = roots.newton_raphson(_f,b,a) 
                    
                    case "Secant":
                        c,_,conv = roots.secant(_f,a,b) 
                    
                if (dropdown.value == "Newton-raphson"):
                    X = np.linspace(a-3,c+3,100)
                else:
                    X = np.linspace(a,b,100)
            
                Y = _f(X)
            
                ax.clear()
                if(not conv):
                    self.error_dialog("tidak konvergen")
                    ax.set_title("Tidak Konvergen")
                else:
                    ax.set_title(f"akar = {c}")
                ax.plot(X,Y)
                ax.scatter(c,_f(c),color='red')
                self.page.update()
            
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return
        
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
        A = ft.TextField(col={"sm":3},label="Matrix A",multiline=True,value="3 1 -1\n2 -2 4\n1 0.5 -1")
        b = ft.TextField(col={"sm":3},label="Matrix b",multiline=True,value="1\n-2\n0")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Gauss-jordan"),
                ft.DropdownOption(key="Gauss-seidel"),
            ],
            value="Gauss-jordan"
        )
        result=ft.Text("",theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        
        def parse_matrix(tf):
            rows = tf.value.strip().split("\n")
            data = [list(map(float, row.split())) for row in rows]
            return np.array(data)

        def parse_vector(tf):
            rows = tf.value.strip().split("\n")
            return np.array([float(r) for r in rows])
     
        def matrix_to_string(v):
            lines = []
            for i, val in enumerate(v, start=1):
                lines.append(f"x{i} = {val}")
            return "\n".join(lines)
        
        def calc(e):
            try:
                _A = parse_matrix(A)
                _b = parse_vector(b)
                match(dropdown.value):
                    case "Gauss-jordan":
                        x=linear.gauss_jordan_tapi_pivot(_A,_b)
                    case "Gauss-seidel":
                            x,_,_=linear.gauss_seidel_safety(_A,_b)
                result.value = matrix_to_string(x)
                self.page.update()
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return
        
        return ft.Container(content=
            ft.Column(
                [
                    ft.Text("Input koefisien persamaan ke matrix A dan b. pastikan format penulisan seperti contoh (dipisahkan dengan spasi dan enter)"),
                    ft.ResponsiveRow(
                        [A,b]
                    ),
                    dropdown,
                    ft.FilledButton("Submit",icon=ft.Icons.CHECK,on_click=calc),
                    result,
                ]
            ),
            alignment=ft.alignment.center
        )

    def __interpolasi_page(self):
        x = ft.TextField(label="x=",value="1,2,5")
        y = ft.TextField(label="y=",value="3,5,0")
        fig,ax = plt.subplots()
        
        def calc(e):
            try:
                _x=[float(i.strip())for i in x.value.split(',')]
                _y=[float(i.strip())for i in y.value.split(',')]
                f = interpolasi.lagrange_polynomial(_x,_y)
                X = np.linspace(_x[0],_x[-1],100)
                Y = [f(i) for i in X]
                ax.clear() 
                ax.scatter(_x,_y,color='red')
                ax.plot(X,Y)
                self.page.update()
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return

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

    def __integral_page(self):
        fx = ft.TextField(label="f(x)=",value="x**2")
        a = ft.TextField(col={"sm":3},label="a=",value="0")
        b = ft.TextField(col={"sm":3},label="b=",value="2")
        n = ft.TextField(col={"sm":3},label="h=",value="4")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Trapezoid"),
                ft.DropdownOption(key="Simpson 1/3"),
                ft.DropdownOption(key="Simpson 3/8"),
            ],
            value="Trapezoid"
        )
        result = ft.Text("Area Under Curve",theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        
        def calc(e):
            try:
                _a = float(a.value.strip())
                _b = float(b.value.strip())
                _n = int(n.value.strip())
                _f = self.make_function(fx.value.strip())
            
                match(dropdown.value):
                    case "Trapezoid":
                        I = integral.trapezoidal_rule(_f,_a,_b,_n)
                    
                    case "Simpson 1/3":
                        I = integral.simpson_one_third(_f,_a,_b,_n)
                    
                    case "Simpson 3/8":
                        I = integral.simpson_three_eight(_f,_a,_b,_n)
                    
            
                result.value = f"Area Under Curve = {I}"
                self.page.update()
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return 
        
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
        x = ft.TextField(label="x=",value="1,2,3,4")
        y = ft.TextField(label="y=",value="2,2,4,5")
        fig,ax = plt.subplots()
        
        def calc(e):
            try:
                _x=[float(i.strip())for i in x.value.split(',')]
                _y=[float(i.strip())for i in y.value.split(',')]
                a,b=regression.linear_regression(_x,_y)
                f = lambda x: a+b*x
            
                Y= [f(i) for i in _x]
                ax.clear()
                ax.set_title(f"f(x)={round(a,4)}+{round(b,4)}x")
                ax.scatter(_x,_y,color='red')
                ax.plot(_x,Y)
                self.page.update()
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return

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
        fx = ft.TextField(label="f(x,y)=",value="x+y")
        x0 = ft.TextField(col={"sm":3},label="x0=",value="0")
        y0 = ft.TextField(col={"sm":3},label="y0=",value="1")
        b  = ft.TextField(col={"sm":3},label="b=",value="0.1")
        h  = ft.TextField(col={"sm":3},label="h=",value="0.005")
        dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="Euler"),
                ft.DropdownOption(key="Heun"),
            ],
            value="Euler"
        )
        result   = ft.Text("Hasil=",theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        
        def calc(e):
            try:
                _f  = self.make_function(fx.value.strip(),xy=True)
                _x0 = float(x0.value.strip())
                _y0 = float(y0.value.strip())
                _b  = float(b.value.strip())
                _h  = float(h.value.strip())
            
                match(dropdown.value):
                    case "Euler":
                        Y = differentiation.euler_method(_f,_x0,_y0,_b,_h)
                    case "Heun":
                        Y = differentiation.heun_method(_f,_x0,_y0,_b,_h)
                result.value = f"Hasil = {Y}"
                self.page.update()
            except Exception as e:
                self.error_dialog(f"ERROR:{e}")
                return

        return ft.Container(content=
            ft.Column(
                [
                    fx,
                    ft.ResponsiveRow(
                        [
                            x0,
                            y0,
                            b,
                            h
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