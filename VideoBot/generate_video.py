import os
import time
import glob
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH")  # Örn: C:/Users/USERNAME/AppData/Local/Google/Chrome/User Data
CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default")
DOWNLOADS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
chrome_options.add_argument(f"profile-directory={CHROME_PROFILE_NAME}")
chrome_options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 20)

def generate_cosmos_story():
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Give a new different story about Cosmos, Astrology and Space Objects in 33 words."}],
        model="llama3-8b-8192",
    )
    story = response.choices[0].message.content + " Under 30 second."
    print("Generated Story:", story)
    return story

def open_invideo_and_generate(cosmos_story):
    driver.get("https://ai.invideo.io/")
    time.sleep(5)

    try_click("//div[contains(text(), 'v3.0')]")
    try_click("//div[contains(text(), 'v2.0')]")
    time.sleep(5)

    input_text("//textarea[@placeholder='Give me a topic, language and detailed instructions']", cosmos_story)
    try_click("//div[text()='Generate a video']")
    time.sleep(20)

    if is_element_present("//p[text()='Retry']"):
        open_veed_and_generate(cosmos_story)
    else:
        try:
            try_click("//div[text()='YouTube shorts']", fallback="//div[text()='Instagram reels']")
            try_click("//div[text()='Continue']")
            download_video_steps()
        except Exception as e:
            print("Shorts/Reels butonunda hata:", e)
            open_veed_and_generate(cosmos_story)

def open_veed_and_generate(cosmos_story):
    driver.get("https://www.veed.io/workspaces/fe73ec84-eeab-41c1-ba4a-fca630f0913f")
    time.sleep(5)

    try_click("//p[text()='AI Text-to-Video']")
    input_text("//textarea[@placeholder='Describe your topic']", cosmos_story)
    close_popup("pop-close")

    try_click("//button[text()='Generate video']", fallback="//div[text()='Voice Only']")
    time.sleep(10)
    wait_for_done_and_download()

def wait_for_done_and_download():

    close_popup("pop-close")
    
    try_click_any({
        "Done": "//span[text()='Done']",
        "Continue": "//button[text()='Continue']",
        "Try again": "//button[text()='Try again']",
    })
    time.sleep(60)

    close_popup("pop-close")

    try_click_any({
        "Done": "//span[text()='Done']",
        "Continue": "//button[text()='Continue']",
        "Try again": "//button[text()='Try again']",
    })

    time.sleep(3)
    done_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='@export/export-button']")))
    done_button.click()
    time.sleep(3)
    close_popup("pop-close")
    time.sleep(3)
    download_button0 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='Download-button-bubble']")))
    download_button0.click()
    time.sleep(3)
    done_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='MP4']")))
    done_button.click()
    time.sleep(30)

def download_video_steps():
    for label in ["Stock watermarks", "Normal", "1080p"]:
        try_click(f"//p[text()='{label}']")
    try_click("//p[text()='Continue']")
    
    try:
        if is_element_present("//p[text()='Export limit reached']"):
            open_veed_and_generate()
    except:
        pass

    try_click("//div[text()='Download']")
    try:
        try_click("//div[text()='Upgrade']")
        open_veed_and_generate()
    except:
        try_click("//div[text()='Download']")
        time.sleep(75)

def input_text(xpath, text):
    elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    elem.send_keys(text)

def try_click(xpath, fallback=None):
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
    except TimeoutException:
        if fallback:
            try_click(fallback)
        else:
            print(f"Element not clickable: {xpath}")

def try_click_any(xpaths_dict):
    for label, xpath in xpaths_dict.items():
        try:
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()
            print(f"Clicked: {label}")
            return label
        except:
            continue
    return None

def is_element_present(xpath):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

def close_popup(class_name):
    try:
        pop = driver.find_element(By.CLASS_NAME, class_name)
        if pop.is_displayed():
            pop.click()
    except:
        pass

def rename_latest_download(cosmos_story):
    latest_file = get_latest_file(DOWNLOADS_PATH)
    if latest_file:
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', ' ', cosmos_story)[:20]
        new_file = append_underscore_if_exists(os.path.join(DOWNLOADS_PATH, f"{safe_name}.mp4"))
        rename_with_retry(latest_file, new_file)

def get_latest_file(path):
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return max(files, key=os.path.getmtime) if files else None

def append_underscore_if_exists(filepath):
    while os.path.exists(filepath):
        base, ext = os.path.splitext(filepath)
        filepath = f"{base}_{ext}"
    return filepath

def rename_with_retry(src, dst, retries=10, delay=2):
    for _ in range(retries):
        try:
            os.rename(src, dst)
            print(f"Renamed file to: {dst}")
            return
        except PermissionError:
            time.sleep(delay)
    print("Failed to rename the file after multiple retries.")

def upload_socials(filename):
    driver.get("https://www.tiktok.com/tiktokstudio/upload")
    time.sleep(5)

    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input.send_keys(filename)

    download_clicked = False  

    max_retries = 10  
    retry_count = 0   

    while not download_clicked and retry_count < max_retries:
        try:
            select_video_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Post']")))
            select_video_button.click()
            download_clicked = True
            print("Post butonuna başarıyla tıklandı.")
        except:
            retry_count += 1  
            print(f"Post butonu henüz tıklanabilir değil, yeniden deniyor... ({retry_count}/{max_retries})")
            time.sleep(15)  

        if not download_clicked:
            print("Post butonuna tıklamak için maksimum deneme sayısına ulaşıldı.")

    time.sleep(15)
    driver.get("https://www.youtube.com/upload")
    time.sleep(5)

    file_input_youtube = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input_youtube.send_keys(filename)

    time.sleep(10)

    radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")))
    radio_button.click()

    time.sleep(1)

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
    next_button.click()

    time.sleep(1)

    next_button1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
    next_button1.click()

    time.sleep(1)

    next_button2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
    next_button2.click()

    time.sleep(1)

    radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='PUBLIC']")))
    radio_button.click()

    time.sleep(5)

    next_button3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Publish']")))
    next_button3.click()
    time.sleep(120)

    driver.get("https://www.instagram.com/")
    time.sleep(5)

    driver.execute_script("document.querySelector('svg[aria-label=\"New post\"]').parentElement.click();")
    file_input_instagram = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input_instagram.send_keys(filename)
    time.sleep(5)

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']")))
    next_button.click()

    time.sleep(1)

    next_button1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Next']")))
    next_button1.click()

    share_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Share']")))
    share_button.click()
    time.sleep(60)
    
def main():
    cosmos_story = generate_cosmos_story()
    open_invideo_and_generate(cosmos_story)
    rename_latest_download(cosmos_story)
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    safe_cosmos_story = re.sub(r'[^a-zA-Z0-9_-]', ' ', cosmos_story)[:20]
    new_filename = os.path.join(downloads_path, f"{safe_cosmos_story}.mp4")
    upload_socials(new_filename)
    driver.quit()

if __name__ == "__main__":
    main()