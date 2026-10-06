import os
import sys

# Attempt to load from the main framework ut_params
try:
    import ut_params
except ImportError:
    # Fallback to sys.path hack if run directly from within a subfolder
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        import ut_params
    except ImportError:
        ut_params = None

UT_TENANT = getattr(ut_params, "UT_TENANT", "at.uibk.ut.tenants")
DITTO_USER = getattr(ut_params, "DITTO_USER", "ditto")
DITTO_PW = getattr(ut_params, "DITTO_PW", "ditto")
DITTO_NGINX_IP = getattr(ut_params, "DITTO_NGINX_IP", "127.0.0.1")

# --- Framework Defaults (Metamorphic Testing) ---
DEFAULT_MIN_CHANGE_PERCENT = 0.01
DEFAULT_MAX_SETTLE_TOLERANCE = 0.01
DEFAULT_SETTLE_TIME = 5.0
DEFAULT_TOLERANCE_FACTOR = 1.2
DEFAULT_ADD_SECONDS = 1
DEFAULT_TIMEOUT = 5.0
DEFAULT_CALIBRATION_RUNS = 1
DEFAULT_CALIBRATION_BASELINE_WAIT = 3.0

DEFAULT_MONITOR_INTERVAL = 10
DEFAULT_RELATION_TOLERANCE = 0.05
DEFAULT_STABILITY_DURATION = 10.0

# --- Pytest & Fixture Defaults ---
DEFAULT_GLOBAL_WAIT_TIME = 30.0

# --- Calibration Logic (Magic Numbers) ---
DEFAULT_CALIBRATION_EPSILON = 0.001
DEFAULT_CALIBRATION_POLL_RATE = 0.02
DEFAULT_CALIBRATION_TIMING_EPSILON = 0.05
