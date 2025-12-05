def euler_method(f,x0,y0,b,h):
    n=(b-x0)/h
    y=y0
    x=x0
    for r in range(int(n)):
        y=y+h*f(x,y)
        x+=h
    return y

def heun_method(f,x0,y0,b,h):
    n=(b-x0)/h
    y=y0
    x=x0
    for r in range(int(n)):
        y_s=y
        y=y+h*f(x,y)
        y=y_s+h/2*(f(x,y_s)+f(x+h,y))
        x+=h
    return y
