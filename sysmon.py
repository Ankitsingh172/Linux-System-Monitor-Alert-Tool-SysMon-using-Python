import psutil
import time
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(
    filename="sysmon.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Thresholds
CPU_THRESHOLD = 80  # percent
MEM_THRESHOLD = 80  # percent
DISK_THRESHOLD = 80  # percent

def log_and_alert(message, level='info'):
    if level == 'warning':
        logging.warning(message)
        print("⚠️", message)
    else:
        logging.info(message)
        print("ℹ️", message)

def get_system_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = time.time() - psutil.boot_time()
    return cpu, memory, disk, uptime

def format_uptime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def monitor():
    log_and_alert("System monitoring started", "info")
    while True:
        cpu, memory, disk, uptime = get_system_usage()
        
        print(f"CPU Usage: {cpu}% | Memory Usage: {memory}% | Disk Usage: {disk}% | Uptime: {format_uptime(uptime)}")

        # Check for threshold crossing
        if cpu > CPU_THRESHOLD:
            log_and_alert(f"High CPU usage detected: {cpu}%", "warning")
        if memory > MEM_THRESHOLD:
            log_and_alert(f"High Memory usage detected: {memory}%", "warning")
        if disk > DISK_THRESHOLD:
            log_and_alert(f"High Disk usage detected: {disk}%", "warning")

        time.sleep(5)  # Delay for next check

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
