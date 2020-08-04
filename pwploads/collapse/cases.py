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


def drill_stem_test_partialevacuation(tvd, rho_mud, tvd_zone, p_zone, g):
    from .pressure_internal import partial_evacuation
    from .pressure_external import onefluid_behindcasing

    p_int = partial_evacuation(tvd, rho_mud, tvd_zone, p_zone, g)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def drill_stem_test_fullevacuation(tvd, rho_mud, g):
    from .pressure_internal import full_evacuation
    from .pressure_external import onefluid_behindcasing

    p_int = full_evacuation(tvd)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def production_fullevacuation(tvd, rho_mud, g):
    from .pressure_internal import full_evacuation
    from .pressure_external import onefluid_behindcasing

    p_int = full_evacuation(tvd)
    p_ext = onefluid_behindcasing(tvd, rho_mud, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def injection_partialevacuation(tvd, tvd_perf, rho_inj, p_inj, p_zone, tvd_influencedzone, rho_fluid_before_cementation,
                                p_fric, rho_form, rho_fluid_above_packer, g):
    from .pressure_internal import partial_evacuation
    from .pressure_external import injection

    p_int = partial_evacuation(tvd, rho_fluid_above_packer, tvd_perf, p_zone, g)
    p_ext = injection(tvd, tvd_perf, p_inj, rho_inj, tvd_influencedzone, rho_fluid_before_cementation, p_fric, rho_form, g)

    pressure_differential = p_int - p_ext

    return pressure_differential


def injection_fulllevacuation(tvd, tvd_perf, rho_inj, p_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form, g):
    from .pressure_internal import full_evacuation
    from .pressure_external import injection

    p_int = full_evacuation(tvd)
    p_ext = injection(tvd, tvd_perf, p_inj, rho_inj, tvd_influencedzone, rho_fluid, p_fric, rho_form, g)

    pressure_differential = p_int - p_ext

    return pressure_differential
