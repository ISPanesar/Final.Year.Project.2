my_pressures = ['Pressure']
my_forces = ['Force']
my_volumetric_flowrates = ['Volumetric Flowrate']
Tube_Diameter = ['Tube Length']


def loop():
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
    Ds = 0.01
    Dt = 0.0001
    mu = 5
    SR = 1
    L = 2
    while (Dt <= 0.02):
        DelP = 4 * L * mu * SR / Dt
        F = DelP * (pi * (Dt/2) ** 2)
        Q = pi * (Dt/2) ** 3 * SR / 4
        my_pressures.append(DelP)
        my_forces.append(F)
        my_volumetric_flowrates.append(Q)
        Tube_Diameter.append(Dt)
        Dt = Dt + 0.0001
    print(DelP)

if __name__ == '__main__':

    try:
        loop()
    except KeyboardInterrupt:
        quit(0)
    final_array = [my_pressures, Tube_Diameter, my_forces, my_volumetric_flowrates]

    import csv

    with open('data.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(final_array)

    csvFile.close()
    quit(0)
