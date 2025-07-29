import os
from datetime import datetime

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    path = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(path)
    print(f" Screenshot saved: {path}")