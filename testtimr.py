from datetime import datetime
import time
current_datetime = datetime.now()
time.sleep(5)
now = datetime.now()
print(now - current_datetime)