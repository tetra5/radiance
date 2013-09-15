# -*- coding: utf-8 -*-


"""
Core calculation/computation functions.
"""


from logic.datatables import AIR_LINEAR_ATTENUATION_COEFFICIENT_X, \
    AIR_LINEAR_ATTENUATION_COEFFICIENT_Y
    
from logic.misc.functions import transpose


def calculate_k_gamma(E, gamma):
    from math import pi
    
    return (3.7 * pow(10, 7) * E * gamma * 1.6 * pow(10, -6) * 3600) / (pi * 4 * 88)


def simulate_layered_screen():
    pass


def simulate_screen(nuclide, d, material, q, r, density):
    # TODO:
    # если mu_d больше 30, p этой энергии приравнять к нулю и пропустить эту линию
    
    from math import exp
    
    from scipy import interpolate
    
    p = 0.0
    p_list = []
    
    b = transpose(material.b)
    
#    print "d:", d
#    print "q:", q
#    print "r:", r
#    print "density:", density
#    print
    
    for s in nuclide.spectre:
        e, n = s
        
        spline = interpolate.splrep(AIR_LINEAR_ATTENUATION_COEFFICIENT_X, 
                                    AIR_LINEAR_ATTENUATION_COEFFICIENT_Y)
        gamma = interpolate.splev(e, spline)
        kgamma = calculate_k_gamma(e, gamma)
        
        spline = interpolate.splrep(material.mass_atten_coeff_x,
                                    material.mass_atten_coeff_y)
        mu = interpolate.splev(e, spline)
        
        mu_d_density = mu * d * density
        
        interp_results = [interpolate.splev(e, interpolate.splrep(material.e, b[i])) 
                          for i in xrange(len(material.mu_d))]
        
        spline = interpolate.splrep(material.mu_d, interp_results)    
        B = interpolate.splev(mu_d_density, spline)
        
        p_line = kgamma * n * exp(-1 * mu_d_density) * B
        
        if p_line < 0:
            p_line = 0
        
        p_list.append((q/pow(r, 2)) * p_line)
        p = p + p_line
        
#        print "e:", e
#        print "n:", n
#        print "mu:", mu
#        print "mu*d*density:", mu_d_density
#        print "B:", B
#        print "p_line:", p_line
#        print "---"
        
    p = (q/pow(r, 2)) * p
    
    return (p, p_list)

