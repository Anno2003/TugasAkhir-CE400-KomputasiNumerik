def trapezoidal_rule(f,a,b,n):
    h=(b-a)/n
    x=a
    I=f(a)+f(b)
    sigma=0
    for r in range(1,n):
        x+=h
        sigma+=2*f(x)
    I=(I+sigma)*h/2

    return I

def simpson_one_third(f,a,b,n):
    # di simpson sepertiga jumlah upaselang (n) harus genap
    if (n%2!=0):
        print(f'upahselang tidak genap!! membulatkan upahselang(n) agar menjadi genap dari {n} jadi {n+1}')
        n+=1
    h=(b-a)/n
    x=a
    I=f(a)+f(b)
    sigma = 0
    for r in range(1,n):
        x+=h
        if (r%2 == 1):
            sigma+=4*f(x)
        else:
            sigma+=2*f(x)
    I=(I+sigma)*h/3
    return I

# TODO: SIMPSON 3/8