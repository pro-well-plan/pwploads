from numpy import interp


def gen_msgs(pipe):
    necessary_inputs = {'Displacement to gas': {'resPressure': 'Reservoir pressure is missing',
                                                'resTvd': 'Reservoir depth (tvd) is missing'},
                        'Production': {'resPressure': 'Reservoir pressure is missing',
                                       'packerTvd': 'Packer depth (tvd) is missing',
                                       'perforationsTvd': 'Depth (tvd) of perforations is missing'},
                        'Injection': {'whp': 'Wellhead Pressure during injection is missing',
                                      'injectionFluid': 'Injection fluid density is missing'},
                        'Pressure Test': {'testFluidDensity': 'Fluid density for pressure test is missing',
                                          'testPressure': 'Testing pressure is missing',
                                          'pipeDiameter': 'Effective pipe diameter is missing'},
                        'Gas Kick': {'resPressure': 'Reservoir pressure is missing',
                                     'resTvd': 'Reservoir depth (tvd) is missing'}}

    missing_loads = {}

    for load, reference in necessary_inputs.items():
        msgs = []
        for parameter, msg in reference.items():
            status = 0

            for section in pipe.settings.values():
                if parameter in section:
                    status = 1

            if status == 0:         # parameter was not found in settings
                msgs.append(msg)

        if len(msgs) > 0:
            missing_loads[load] = msgs

    pipe.msgs = missing_loads


def define_max_loads(loads):
    for load in loads:
        min_level = {'force': min(load['axialForce']), 'pressure': min(load['diffPressure'])}
        max_level = {'force': max(load['axialForce']), 'pressure': max(load['diffPressure'])}
        max_loads = {}

        if min_level['force'] < 0:
            max_loads['compression'] = min_level['force']
        else:
            max_loads['compression'] = None

        if max_level['force'] > 0:
            max_loads['tension'] = max_level['force']
        else:
            max_loads['tension'] = None

        if min_level['pressure'] < 0:
            max_loads['collapse'] = min_level['pressure']
            load['_MaxCollapsePoint'] = load['axialForce'][load['diffPressure'].index(min_level['pressure'])]
        else:
            max_loads['collapse'] = None

        if max_level['pressure'] > 0:
            max_loads['burst'] = max_level['pressure']
        else:
            max_loads['burst'] = None

        load['maxLoads'] = max_loads


def get_collapse_base(csg, axial_force):
    if axial_force <= 0:
        collapse_base = csg.limits['collapse']
    else:
        collapse_base = interp(axial_force, csg.ellipse[0], csg.ellipse[2])
    return collapse_base


def define_min_df(csg):
    base = {'compression': csg.conn_limits[0], 'tension': csg.conn_limits[1], 'burst': csg.limits['burst']}

    for load in csg.loads:
        if '_MaxCollapsePoint' in load:
            base['collapse'] = get_collapse_base(csg, load['_MaxCollapsePoint'])
        load['minDF'] = {}
        for load_type, value in load['maxLoads'].items():
            if value is None:
                load['minDF'][load_type] = None
            else:
                load['minDF'][load_type] = base[load_type] / value


def define_safety_factors(csg):
    precaution = {'burst': None, 'collapse': None, 'tension': None, 'compression': None}
    for load_type in precaution.keys():
        warning = {'load': None, 'safetyFactor': 1000, 'maxLoad': None}
        for load in csg.loads:
            if load['minDF'][load_type] is None:
                value = 1000
            else:
                value = load['minDF'][load_type]
            if value < warning['safetyFactor']:
                warning['load'] = load['description']
                warning['safetyFactor'] = round(load['minDF'][load_type], 2)
                warning['maxLoad'] = round(abs(load['maxLoads'][load_type]), 2)
                precaution[load_type] = warning

    csg.safety_factors = precaution
