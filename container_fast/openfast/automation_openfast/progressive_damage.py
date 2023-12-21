def increasing_mass_imbalance(blade_file, adjusting_factor):
    with open(blade_file, "r") as blade_properties:
        lines = blade_properties.read().splitlines()
        mass_density = lines[10].split()
        new_mass = round(float(mass_density[0]), 4) + adjusting_factor
        lines[10] = f"          {str(new_mass)}   AdjBlMs     - Factor to adjust blade mass density (-)"

    with open(blade_file, 'w') as new_blade:
        new_blade.write('\n'.join(lines))


def increasing_airfoil_erosion(airfoil_file, cl_reducing_factor, cd_rising_factor):

    with open(airfoil_file, "r") as airfoil_properties:
        lines = airfoil_properties.read().splitlines()
        for line in range(55, 112):
            line_list = lines[line].split()
            new_cl = float(line_list[1]) - ((cl_reducing_factor * float(line_list[1])) / 100)
            new_cd = float(line_list[2]) + ((cd_rising_factor * float(line_list[2])) / 100)
            lines[line] = f"    {line_list[0]}   {new_cl}    {new_cd}"
        with open(airfoil_file, 'w') as new_airfoil:
            new_airfoil.write('\n'.join(lines))


def increasing_aerodata_erosion(aerodata_file, cl_reducing_factor, cd_rising_factor):
    
    with open(aerodata_file, "r") as aerodata_properties:
        lines = aerodata_properties.read().splitlines()
        for line in range(14, 70):
            line_list = lines[line].split()
            new_cl = float(line_list[1]) - ((cl_reducing_factor * float(line_list[1])) / 100)
            new_cd = float(line_list[2]) + ((cd_rising_factor * float(line_list[2])) / 100)
            lines[line] = f"    {line_list[0]}   {new_cl}    {new_cd}"
        with open(aerodata_file, 'w') as new_aerodata:
            new_aerodata.write('\n'.join(lines))
