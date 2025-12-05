import numpy as np

def gauss_jordan_tapi_pivot(A,b):
    x = np.zeros_like(b)
    A = np.hstack((A, b.reshape(-1, 1)))
    n=A.shape[0]
    for k in range(n):
        ######
        pivot_row = k
        max_value = abs(A[k,k])
        for i in range(k+1,n):
            if abs(A[i,k]) > max_value:
                max_value = abs(A[i,k])
                pivot_row = i

        if pivot_row != k :
            A[[k, pivot_row]] = A[[pivot_row, k]]
            print("pivot!")
            print(A)

        if (A[k,k] == 0):
            print("no unique solution (singular matrix)")
            return None,i,False
        #######
        pivot = A[k,k]
        for j in range (n+1):
            A[k,j]=A[k,j]/pivot

        for i in range (n):
            if i != k :
                factor = A[i,k]
                for j in range (k,n+1):
                    A[i,j]=A[i,j]-factor*A[k,j]
            print(A)
    for i in range(n):
        x[i]=A[i][n]

    return x

def gauss_seidel_safety(A,b,tol=0.0000000001,max_iter=1000):
    dominasi=False
    epsilon = tol
    x=np.zeros_like(b)
    xlama=np.zeros_like(b)
    n=A.shape[0]
    konvergen = False
    # cek dominasi duls


    d=abs(A[0,0])
    e=abs(A[0,1])
    if (d<e):
        dominasi=True
    d=abs(A[1,1])
    e=abs(A[1,0])
    if (d<e):
        dominasi=True
    if dominasi:
        print("terjadi dominasi diagonal persamaan tdk bisa konvergen")
        return None,0,False
    for z in range (max_iter):
        for i in range(n):
            xlama[i]=x[i]
            sigma1=0
            for j in range(i):
                sigma1=sigma1+A[i,j]*x[j]
            sigma2=0
            for j in range(i+1,n):
                sigma2=sigma2+A[i,j]*x[j]
            x[i]=(b[i]-sigma1-sigma2)/A[i,i]
        konvergen = True
        i=0
        while (konvergen and i<n):
            if abs(xlama[i]-x[i])>epsilon:
                konvergen=False
            i=i+1

        if konvergen:
            return x,i,True
    return None,max_iter,False