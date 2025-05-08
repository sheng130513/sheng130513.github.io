
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#%% 
#參考 SelExample_tpe+dcard.py (台北市政府開放資料庫)
def extract_page_data():
    time.sleep(1)
    items = driver.find_elements(By.CSS_SELECTOR, "div[class='_iQpvk1c9OgRAc8KRTlH']") 
    for item in items[:15]: #取前15項
        title_element = item.find_element(By.TAG_NAME, "a") 
        title = title_element.text
        link = title_element.get_attribute("href")
        data_list.append({"歌名": title, "連結": link})
        print(title, link)


#%%
a = input("請輸入想搜尋的歌手：")
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
    options=options
)
# 啟動瀏覽器
driver.get("https://open.spotify.com/" )
driver.maximize_window()

# 搜尋關鍵字
search_box = driver.find_element(By.CSS_SELECTOR, 'input[class="e-9890-form-input e-9890-baseline e-9890-form-control encore-text-body-medium CVuGEUIxLkNKpMds8AFS R69APjfNV0o9tAbfrWZf"]') 
search_box.send_keys(a)
search_box.send_keys(Keys.ENTER)
time.sleep(1)

#參考 SelExample_twrailway.py (台鐵時刻表)
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@data-testid='see-all-link' and text()='歌曲']")
            )
        ).click()
    time.sleep(3)
except Exception as e:
    print("點擊歌曲連結失敗：", e)

# 存放所有資料的列表
data_list = []

print('Spotify中歌手 "'+a+'" 的前15首歌曲')
extract_page_data()


driver.quit()


#%%
import pandas as pd
# 轉為 DataFrame 並輸出成 CSV
df = pd.DataFrame(data_list)
df.to_csv(r"C:/Users/USER/Desktop/q86/Spotify.csv", index=False, encoding="utf-8-sig")




