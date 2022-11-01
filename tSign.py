import os,time
from selenium import webdriver
from mail_spider import Spider as mailSpider
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException 
from selenium.common.exceptions import TimeoutException as SeleTimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from configparser import ConfigParser

class TSign:
    def __init__(self):     
        cfg = ConfigParser()
        cfg.read('config.ini')
        self.certsign_username = cfg.get('certsign', 'username')
        self.certsign_password = cfg.get('certsign', 'password')
        self.iflow_username = cfg.get('iflow', 'username')
        self.iflow_password = cfg.get('iflow', 'password')
        self.email_username = cfg.get('email', 'username')
        self.email_password = cfg.get('email', 'password')
        self.coeff11n = cfg.get('iflow', '11n')
        self.coeff11ac = cfg.get('iflow', '11ac')
        self.coeff11ax = cfg.get('iflow', '11ax')
        self.mspt_usr = cfg.get('ms_sign', 'username')
        self.mspt_pwd = cfg.get('ms_sign', 'password')
        #current_path = os.path.dirname(os.path.realpath(__file__))
    
    def initBrowser(self):
        current_path = os.path.abspath('.')
        driver_path=current_path + r"\chromedriver.exe"
        #self.driver=webdriver.Chrome(executable_path=driver_path)
        print("driver_path=", driver_path)
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
            'download.default_directory': 'd:\\'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    
    def signFiles(self, data):
        self.initBrowser()
        driver = self.driver
        driver.get("https://certsign.realtek.com/Login.jsp")
        login_username = driver.find_element_by_xpath("//*[@id=\"login_username\"]")
        login_password = driver.find_element_by_xpath("//*[@id=\"login_password\"]")
        btnLogin = driver.find_element_by_xpath("//*[@id=\"btnLogin\"]")
        login_username.send_keys(self.certsign_username)
        login_password.send_keys(self.certsign_password)
        btnLogin.click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"getOTP\"]").click()
        mailspr = mailSpider()
        optcode = mailspr.dl_mail(self.email_username, self.email_password)
        time.sleep(3)
        if optcode is not None:
            print(" ============== (*-*) ==================")
            driver.find_element_by_xpath("//*[@id=\"otp1\"]").send_keys(optcode)
            driver.find_element_by_xpath("//*[@id=\"validOTP\"]").click()
            time.sleep(0.2)
            
            for finfo in  data:
                filename = finfo["filename"]
                #driver.find_element_by_xpath("//span[@class='buttonText'][contains(.,'Choose file')]").click()
                driver.find_element_by_xpath("//input[@type='file']").send_keys(filename)
                #driver.find_element_by_xpath("//input[@type='file']").send_keys(r"D:\xv\MP_branch\8822c\8822c\RTLWlanU_WindowsDriver_\Win7.zip")
                i = 0
                while True:
                    try:
                        driver.find_element_by_xpath("//button[@type='button'][contains(.,'上傳檔案')]").click()
                        time.sleep(6)
                        i=1
                    except SeleTimeoutException as e:
                        print("raise exception 上傳檔案 time out")
                    finally:
                        if i > 0:
                            break
                
                s = driver.find_element_by_xpath("//select[contains(@name,'shaType')]")
                Select(s).select_by_value('9E2E281E-BE0A-43E1-899A-2B2B2EA5D0FA') #EVSign  SHA256演算法
                '''
                //#EVSign  SHA256演算法
                // 8B4F20EC - DB9A - 49FB - 9722 - 7A4E3F9EE077 EVSign SHA1演算法
                // D03E8893 - CBC6 - 4567 - 8781 - 430A30FA6CC3 EVSign SHA256演算法(Append)
                //  D75001C2 - 141D - 42E9 - 9CED - 41A62A8FD0E2 EVSign SHA1演算法 & amp; SHA256演算法
                '''
                driver.find_element_by_xpath("//button[@type='button'][contains(.,'簽署憑證')]").click()
                time.sleep(3)
                for i in range(0, 10):
                    try:
                        driver.find_element_by_xpath("//strong[contains(.,'已完成簽署!')]")
                        break;
                    except  NoElementFoundException:
                        print("未签署完成，3秒后重试 =============>")
                        time.sleep(3)
                        
                element = driver.find_element_by_xpath("//button[@type='button'][contains(.,'Download')]")
                element = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, "//button[@type='button'][contains(.,'Download')]")))
                ActionChains(self.driver).move_to_element(element).click().perform()
        
    def MSSign(self, data):
        self.initBrowser()
        driver = self.driver
        while (True):
            try:
                driver.get("https://partner.microsoft.com/zh-CN/dashboard/hardware/Search")
                    #https://partner.microsoft.com/zh-CN/dashboard/hardware/Search
                time.sleep(6);
                login_username = driver.find_element_by_xpath("//input[contains(@type,'email')]")
                login_username.send_keys(self.mspt_usr);
                time.sleep(0.1);
                next_btn = driver.find_element_by_xpath("//input[contains(@type,'submit')]")
                next_btn.click();
                time.sleep(2);
                login_password = driver.find_element_by_xpath("//input[contains(@name,'passwd')]")
                login_password.send_keys(self.mspt_pwd);
                next_btn = driver.find_element_by_xpath("//input[contains(@type,'submit')]")
                next_btn.click();
                time.sleep(1);
                next_btn = driver.find_element_by_xpath("//input[contains(@value,'是')]")
                next_btn.click();
                time.sleep(1);
           
                for needSignItem in data:
                    retry = 0;
                    driver.get("https://partner.microsoft.com/zh-CN/dashboard/hardware/driver/New")
                    '''
                    next_btn = driver.find_element_by_xpath("//div[@class='onedash-navigation-category'][contains(.,'驅動程式')]")
                    next_btn = driver.find_element_by_xpath("//A[@href='/zh-tw/dashboard/hardware/driver'][text()='驅動程式']")
                    next_btn.Click();
                    '''
                    time.sleep(6)
                    while(True):
                        try:
                            #IWebElement newhard = driver.find_element_by_xpath("//A[@class='btn btn-primary hide-focus'][text()='Submit new hardware']")
                            #newhard.click();
                            inputHN = driver.find_element_by_xpath("//*[@id=\"inputDriverName\"]")
                            inputHN.send_keys(needSignItem["proj_name"])
                            inputfile = driver.find_element_by_xpath("//*[@id='file']")
                            inputfile.send_keys(needSignItem["filename"])
                            time.sleep(5)
     
                            WebDriverWait(driver,10).until(EC.visibility_of_element_located(('xpath',"//span[@uitestid='spanRequestedSignature_WINDOWS_v100_X64_RS1_FULL']")))
                            if (needSignItem["isX64"]):
                                checkBox_X64_RS1 = driver.find_element_by_xpath("//span[@uitestid='spanRequestedSignature_WINDOWS_v100_X64_RS1_FULL']")
                                checkBox_X64_19H1 = driver.find_element_by_xpath("//span[@uitestid='spanRequestedSignature_WINDOWS_v100_X64_19H1_FULL']")
                                checkBox_X64_RS1.click()
                                checkBox_X64_19H1.click()
                            else:
                                checkBox_X86_RS1 = driver.find_element_by_xpath("//span[contains(@uitestid,'spanRequestedSignature_WINDOWS_v100_RS1_FULL')]")
                                checkBox_X86_19H1 = driver.find_element_by_xpath("//span[contains(@uitestid,'spanRequestedSignature_WINDOWS_v100_19H1_FULL')]")
                                checkBox_X86_RS1.click()
                                checkBox_X86_19H1.click()
                            
                            time.sleep(10);
                            while (True):
                            
                                try:

                                    WebDriverWait(driver=driver,timeout=10,poll_frequency=0.5).until(\
                                        expected_conditions.visibility_of_element_located(('xpath',"//button[@uitestid='buttonSubmit']"))\
                                    )
                                    break
                                except SeleTimeoutException as ste:
                                    time.sleep(2)
                                                        

                            submit_btn = driver.find_element_by_xpath("//button[@uitestid='buttonSubmit']")
                            submit_btn.click()
                            time.sleep(20)
                            break
                        
                        except ElementNotInteractableException as enie:
                                continue
                        except (NoSuchElementException, ElementClickInterceptedException) as nseex:
                            print(nseex.toString())
                            driver.get("https://partner.microsoft.com/zh-CN/dashboard/hardware/driver/New")
                            time.sleep(5)
                            continue
                break
            except NoSuchElementException as nseex :

                    print(nseex.toString())
                    time.sleep(2)
                    continue

        
    