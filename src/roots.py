
def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Bisection method for root finding.
    f : function
    a, b : interval [a,b]
    tol : tolerance for stopping
    max_iter : maximum number of iterations
    """
    if f(a) * f(b) > 0:
        raise ValueError("Bisection method fails: f(a) and f(b) have the same sign.")

    for i in range(max_iter):
        c = (a + b) / 2.0
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c, i+1, True
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, max_iter, False  # did not converge

def regula_falsi_gacor (f,a,b,tol=1e-7,max_iter=1000):
    iters=[]

    simpan = 0
    mandek_kiri = 1
    mandek_kanan = 1
    FA=f(a)
    FB=f(b)

    for i in range(max_iter):
        c=b-(FB*(b-a)/(FB-FA))
        iters.append([a,b,c,f(c)])

        print(f"{i}|A:{a}|B:{b}|C:{c}|f(c):{f(c)}")

        if abs(f(c))<tol:
            a=c
            b=c
        else:
            if f(a)*f(c)<0:
                b=c
                FB=f(c)
                mandek_kiri+=1
                mandek_kanan=0
                if mandek_kiri>0:
                    FA=FA/2
            else:
                a=c
                FA=f(c)
                mandek_kanan+=1
                mandek_kiri=0
                if mandek_kanan>1:
                    FB=FB/2
        if abs(a-b)<tol:
            return c,i,True,iters
    return c,i,False,iters

def newton_raphson(f,df,x0,tol=0.0001,max_iter=10000):
    x_sebelumnya= 0

    for i in range(max_iter):
        if (abs(df(x0))<tol):
            print('pembagian dengan bilangan mendekati 0')
            return x0,i,True
        else:
            x_sebelumnya=x0
            x0=x0-f(x0)/df(x0)
        if((abs(x0-x_sebelumnya)<tol)):
            return x0,i,True
        # print(f"{i}|{f(x0)} {df(x0)}")
    print('divergen!')
    return None,i,False

def secant(f,x0,x1,tol=0.0001,max_iter=10000):
    for i in range(max_iter):
        if (abs(f(x1)-f(x0))<tol):
            print('pembagian dengan bilangan mendekati 0')
            return x1,i,True
        else:
            x=x1-(f(x1)*(x1-x0)/(f(x1)-f(x0)))
            x0=x1
            x1=x
        if((abs(x0-x1)<tol)):
            return x1,i,True
        # print(f"{i}|{f(x0)} {f(x1)}")
    print('divergen!')
    return None,i,False
