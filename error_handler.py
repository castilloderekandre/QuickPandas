import sys
import os
import datetime
import traceback
from CTkMessagebox import CTkMessagebox

def log_error_to_file(type, value, tb):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join("logs", f"reportwise_{timestamp}.log")

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {type.__name__}: {value}\n")
        # traceback.print_exception(type, value, tb, file=f)
        traceback.print_tb(tb, file=log_file)
        log_file.write("\n")


def show_exception_popup(type, value, tb) -> None:
    """
    Shows a popup through CTkMessagebox for an unhandled exception.

    Args:
        type (ERROR TYPE): exception class.
        value (ERROR TYPE): exception instance.
        tb (ERROR TYPE): traceback.

    Returns:
        nothing
    """
    # Log it first
    log_error_to_file(type, value, tb)

    # Then show popup
    msg = f"{type.__name__}: {value}"
    CTkMessagebox(title="Unhandled Exception", message=msg, icon="cancel")

def install_global_handler():
    sys.excepthook = show_exception_popup


