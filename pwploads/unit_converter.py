def convert_unit(value, unit_from="ft", unit_to="m"):

    result = 0
    conversion = False

    if type(value) != list:
        value = [value]

    # Length
    if (unit_from == "ft") and (unit_to == "m"):
        conversion = True
        result = [x / 3.281 for x in value]

    if (unit_from == "m") and (unit_to == "ft"):
        conversion = True
        result = [x * 3.281 for x in value]

    if (unit_from == "in") and (unit_to == "m"):
        conversion = True
        result = [x / 39.37 for x in value]

    if (unit_from == "m") and (unit_to == "in"):
        conversion = True
        result = [x * 39.37 for x in value]

    # AREA
    if (unit_from == "in2") and (unit_to == "m2"):
        conversion = True
        result = [x/1550 for x in value]

    if (unit_from == "m2") and (unit_to == "in2"):
        conversion = True
        result = [x*1550 for x in value]

    # Pressure
    if (unit_from == "Pa") and (unit_to == "bar"):
        conversion = True
        result = [x/1e5 for x in value]

    if (unit_from == "bar") and (unit_to == "Pa"):
        conversion = True
        result = [x*1e5 for x in value]

    if (unit_from == "Pa") and (unit_to == "psi"):
        conversion = True
        result = [x/6895 for x in value]

    if (unit_from == "psi") and (unit_to == "Pa"):
        conversion = True
        result = [x/6895 for x in value]

    if (unit_from == "N/mm2") and (unit_to == "bar"):
        conversion = True
        result = [x*10 for x in value]

    if (unit_from == "bar") and (unit_to == "N/mm2"):
        conversion = True
        result = [x/10 for x in value]

    if (unit_from == "psi") and (unit_to == "bar"):
        conversion = True
        result = [x/14.504 for x in value]

    if (unit_from == "bar") and (unit_to == "psi"):
        conversion = True
        result = [x*14.504 for x in value]

    # Density
    if (unit_from == "kg/m3") and (unit_to == "sg"):
        conversion = True
        result = [x/1000 for x in value]

    if (unit_from == "sg") and (unit_to == "kg/m3"):
        conversion = True
        result = [x*1000 for x in value]

    if (unit_from == "lb/in3") and (unit_to == "sg"):
        conversion = True
        result = [x*27.68 for x in value]

    if (unit_from == "sg") and (unit_to == "lb/in3"):
        conversion = True
        result = [x/27.68 for x in value]

    # Force
    if (unit_from == "kN") and (unit_to == "lbf"):
        conversion = True
        result = [x * 1000 / 4.448 for x in value]

    if (unit_from == "lbf") and (unit_to == "kN"):
        conversion = True
        result = [x * 4.448 / 1000 for x in value]

    if len(result) == 1:
        result = result[0]

    if not conversion:
        print("No conversion has been done")

    return result
