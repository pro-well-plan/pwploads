def drilling_losses(tvd, rho_mud, tvd_zone, p_zone, g):
    from .pressure_internal import partial_evacuation
    from .pressure_external import onefluid_behindcasing

    p_int = partial_evacuation(tvd, rho_mud, tvd_zone, p_zone, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def plug_cementation_onefluid_behindcasing(tvd, rho_fluid, rho_mud, g):
    from .pressure_internal import inside_full
    from .pressure_external import onefluid_behindcasing

    p_int = inside_full(tvd, rho_fluid, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def plug_cementation_morefluids_behindcasing(tvd, rho_fluid, tvd_fluid, g):
    from .pressure_internal import inside_full
    from .pressure_external import morefluids_behindcasing

    p_int = inside_full(tvd, rho_fluid, g)
    p_ext = morefluids_behindcasing(tvd, rho_fluid, tvd_fluid, g)

    pressure_differential = p_int - p_ext

    return pressure_differential



