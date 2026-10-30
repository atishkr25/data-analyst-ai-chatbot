import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

output_dir = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\data-analyst-ai-chatbot\screenshots")
output_dir.mkdir(parents=True, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1366,860")

driver = webdriver.Chrome(options=options)

pages = [
    ("screenshot_1_upload.png", "http://localhost:8501/?page=Upload+Dataset"),
    ("screenshot_2_dashboard.png", "http://localhost:8501/?page=Dashboard"),
    ("screenshot_3_explorer.png", "http://localhost:8501/?page=Data+Explorer"),
    ("screenshot_4_chatbot.png", "http://localhost:8501/?page=AI+Chatbot"),
    ("screenshot_5_sql.png", "http://localhost:8501/?page=SQL+Explorer"),
    ("screenshot_6_insights.png", "http://localhost:8501/?page=Insights"),
]

print("Starting screenshot capture from running Streamlit application...")

for filename, url in pages:
    driver.get(url)
    # Wait for Streamlit rendering and plotly/tables
    time.sleep(4)
    save_path = output_dir / filename
    driver.save_screenshot(str(save_path))
    file_size = save_path.stat().st_size
    print(f"Captured {filename}: {file_size:,} bytes")

driver.quit()
print("All screenshots successfully captured!")
