def get_conn_limits(limits, conn_compression=0.6, conn_tension=0.6, df_conn_compression=1.0,
                    df_conn_tension=1.0):

    tension_limit = limits['tension']
    compression_limit = limits['compression']

    conn_compression_limit = compression_limit * conn_compression / df_conn_compression
    conn_tension_limit = tension_limit * conn_tension / df_conn_tension

    return [conn_compression_limit, conn_tension_limit]
