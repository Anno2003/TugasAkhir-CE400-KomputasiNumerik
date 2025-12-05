def linear_regression(x,y):
    n=len(x)
    s_x = np.sum(x)
    s_x2 = []
    s_y = np.sum(y)
    s_xy = []
    for i in range(n):
        s_xy.append(x[i]*y[i])
        s_x2.append(x[i]**2)
    s_xy = np.sum(s_xy)
    s_x2 = np.sum(s_x2)
    yntkts = s_x**2

    b = (n*s_xy - s_x*s_y)/(n*s_x2-yntkts)
    a = np.mean(y)-b*np.mean(x)

    return a,b