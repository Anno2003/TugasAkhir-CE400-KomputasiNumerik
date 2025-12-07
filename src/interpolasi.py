# TODO: lagrange interpolation
#

def lagrange_polynomial(x_values, y_values):
    n = len(x_values)

    def P(x):
        total = 0
        for i in range(n):
            term = y_values[i]
            for j in range(n):
                if i != j:
                    term *= (x - x_values[j]) / (x_values[i] - x_values[j])
            total += term
        return total

    return P