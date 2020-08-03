# meta
log_levels = dict(
    critical='CRITICAL',
    error='ERROR',
    warning='WARNING',
    info='INFO',
    debug='DEBUG'
)

general = dict(
    log_level=log_levels["debug"],
    log_file_name="teapot.log",
    max_log_size=1024 * 1024 * 10,  # Bytes
    max_log_file_count=3,
)
