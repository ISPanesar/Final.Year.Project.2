class Calc:
    from sympy.solvers import solvers
    from sympy import Symbol
    DeltaP = Symbol('DelP')
    Length = Symbol('L')
    Diameter_of_Syringe = Symbol('Ds')
    Diameter_of_Tube = Symbol('Dt')
    Viscosity = Symbol('mu')
    pi = 3.14195
    Strain_Rate = Symbol('SR')
    Velocity_Tube = Symbol('vt')
    Velocity_Syringe = Symbol('vs')
    Volumetric_Flowrate = Symbol('Q')
    Force = Symbol('F')
    L = float(input('How long is the tubing in meters?'))
    Ds = float(input('What is the diameter of the syringe in meters?'))
    Dt = float(input('What is the diamater of the tube in meters?'))
    mu = float(input('What is the viscosity of the fluid in Pascal seconds?'))
    SR = float(input('What is the strain rate in per second?'))
    vt = SR * L
    Q = vt * pi * (Dt / 2) ** 2
    vs = Q / (pi * (Ds / 2) ** 2)
    DelP = 32 * mu * L * vt / (Dt ** 2)
    F = DelP / (pi * (Dt/2) ** 2)
    print('vt')
    print(vt)
    print('vs')
    print(vs)
    print('Q')
    print(Q)
    print('DelP')
    print(DelP)
    print('F')
    print(F)
