import sys
import os
import datetime
import traceback
from CTkMessagebox import CTkMessagebox

# sys.stdout = open(log_path, "w", encoding='utf-8')
# sys.stderr = sys.stdout

print(f"Logging started at {datetime.datetime.now()}")
print(f"Log file: {log_path}\n")

LOG_FILE = "error.log"

def log_error_to_file(exc_type, exc_value, exc_traceback):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join("logs", f"reportwise_{timestamp}.log")

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {exc_type.__name__}: {exc_value}\n")
        # traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        traceback.print_tb(exc_traceback, file=log_file)
        log_file.write("\n")

def show_exception_popup(exc_type, exc_value, exc_traceback):
    # Log it first
    log_error_to_file(exc_type, exc_value, exc_traceback)

    # Then show popup
    msg = f"{exc_type.__name__}: {exc_value}"
    CTkMessagebox(title="Unhandled Exception", message=msg, icon="cancel")

def install_global_handler():
    sys.excepthook = show_exception_popup


