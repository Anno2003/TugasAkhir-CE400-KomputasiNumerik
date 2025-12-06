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

def simpson_three_eight(f, a, b, n):
    # n must be a multiple of 3
    if n % 3 != 0:
        fixed_n = n + (3 - (n % 3))
        print(f'upahselang (n) harus kelipatan 3! dibulatkan dari {n} menjadi {fixed_n}')
        n = fixed_n

    h = (b - a) / n
    I = f(a) + f(b)
    sigma = 0
    x = a

    for r in range(1, n):
        x += h
        # Coefficients for 3/8 rule:
        # r % 3 == 0 → coefficient 2
        # otherwise → coefficient 3
        if r % 3 == 0:
            sigma += 2 * f(x)
        else:
            sigma += 3 * f(x)

    I = (I + sigma) * (3 * h) / 8
    return I
