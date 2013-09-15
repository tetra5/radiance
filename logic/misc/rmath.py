def lagrange_poly(x, y, value):
    
    n = len(x)

    if len(y) is not n:
        raise Exception, "Input lists length mismatch."

    s = 0.0

    for i in xrange(n):
        w = 1.0

        for j in xrange(n):
            if j == i:
                continue
            w *= (value - x[j]) / (x[i] - x[j])
        s += w * y[i]

    return s


class CubicSpline(object):
    """
    Cubic spline interpolation.
    Usage:
    
    @param x: list of x values
    @param y: list of corresponding y values
    @param value: value to interpolate 
    
    Both input lists must be of the same length.
    
    s = CubicSpline(x, y)
    result = s.interpolate(value)
    
    or
    
    result = CubicSpline(x, y).interpolate(value)
    
    or
    
    result = CubicSpline(x, y)(value)
    
    """
    
    def __init__(self, x=None, y=None):
        self.__splines = []

        if x is not None and y is not None:
            self.build(x, y)

    def build(self, x, y):
        
        n = len(x)

        if len(y) is not n:
            raise Exception, "Input lists length mismatch."

        for i in xrange(n):
            self.__splines.append(dict(a=y[i], b=0.0, c=0.0, d=0.0, x=x[i]))

        alpha = [0.0]
        beta = [0.0]

        for i in xrange(1, n - 1):
            h_i = x[i] - x[i - 1]
            h_i1 = x[i + 1] - x[i]
            C = 2.0 * (h_i + h_i1)
            F = 6.0 * ((y[i + 1] - y[i]) / h_i1 - (y[i] - y[i - 1]) / h_i)
            z = h_i * alpha[i - 1] + C
            alpha.append(-h_i1 / z)
            beta.append((F - h_i * beta[i - 1]) / z)

        for i in reversed(xrange(n - 1)):
            self.__splines[i]['c'] = alpha[i] * self.__splines[i + 1]['c'] + beta[i]

        for i in reversed(xrange(n)):
            h_i = x[i] - x[i - 1]
            self.__splines[i]['d'] = \
                (self.__splines[i]['c'] - self.__splines[i - 1]['c']) / h_i
            self.__splines[i]['b'] = \
                h_i * (2.0 * self.__splines[i]['c'] + self.__splines[i - 1]['c']) / \
                    6.0 + (y[i] - y[i - 1]) / h_i

        return self

    def interpolate(self, value):
        
        if not self.__splines:
            raise Exception, "Splines are not calculated yet."

        n = len(self.__splines)

        if value <= self.__splines[0]['x']:
            s = self.__splines[1]
        elif value >= self.__splines[n - 1]['x']:
            s = self.__splines[n - 1]
        else:
            i = 0
            j = n - 1
            while(i + 1 < j):
                k = i + (j - i) / 2
                if value <= self.__splines[k]['x']:
                    j = k
                else:
                    i = k
            s = self.__splines[j]

        dx = value - s['x']

        return s['a'] + (s['b'] + (s['c'] / 2.0 + s['d'] * dx / 6.0) * dx) * dx
    
    def __call__(self, value):
        
        return self.interpolate(value)
        
    
if __name__ == '__main__':
    
    x = [0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.66, 0.70, 0.80, 1.00, 1.25, 1.5, 2.00, 3.00]
    y = [45.5, 22.6, 8.75, 4.96, 3.38, 2.55, 2.30, 2.15, 1.76, 1.39, 1.15, 1.0, 0.89, 0.81]
    
    value = 0.211112344123
    
    print x
    print y

    print "Cubic spline interpolation of %.2f:" % value, \
        CubicSpline(x, y)(value)
        #CubicSpline(x, y).interpolate(value)
    print "Lagrange interpolation of %.2f:" % value, \
        lagrange_poly([0.15, 0.20, 0.30, 0.40, 0.50], [45.5, 22.6, 8.75, 4.96, 3.38], 
                      value)
    
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [k**2 for k in x]
    value = 2000
    
    print CubicSpline(x, y).interpolate(value)
    print lagrange_poly(x, y, value)
    