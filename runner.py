import subprocess
import time
DELAY = 10

while True:
    subprocess.call("python3 get_cse_home_data.py", shell=True)
    subprocess.call("python3 get_latest_item_updates.py", shell=True)
    subprocess.call("python3 get_market_movers.py", shell=True)
    subprocess.call("python3 get_latest_news.py", shell=True)
    subprocess.call("python3 get_top_ten_gainers_losers.py", shell=True)
    subprocess.call("python3 get_dse_home_data.py", shell=True)

    time.sleep(DELAY)


