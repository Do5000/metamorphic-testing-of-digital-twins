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
