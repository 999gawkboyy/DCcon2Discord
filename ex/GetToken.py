from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
from ex import WriteToken

def Get(email, pwd) :
    try :
        f = open("token.txt", "r")
        token = f.readline()
        print(token)
        return token
    except :
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        try:
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
        except:
            chromedriver_autoinstaller.install(True)
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--incognito")
        mobile_emulation = { "deviceName": "iPhone X" }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://discord.com/login')
        time.sleep(2)

        element = driver.find_element(By.NAME, 'email')
        element.send_keys(email)

        element = driver.find_element(By.NAME, 'password')
        element.send_keys(pwd)

        element = driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')
        element.click()
        time.sleep(5)
        driver.execute_script("""
        function getLocalStoragePropertyDescriptor() {
            const iframe = document.createElement('iframe');
            document.head.append(iframe);
            const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
            iframe.remove();
            return pd;
        }
        
        Object.defineProperty(window, 'localStorage', getLocalStoragePropertyDescriptor());

        const localStorage = getLocalStoragePropertyDescriptor().get.call(window);""")
        token = driver.execute_script("return window.localStorage.getItem('token')")
        print('lodaing ...')
        WriteToken.WriteToken(token[1:-1])
        return token[1:-1]