from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from backup import save


class Chrome:

    def __init__(self):
        print('\n\nOIE!!\n Bora rodar..')
        self.ser = Service('chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.ser,
                                       chrome_options=self.option)


    def bye(self):
        self.driver.close()
        print('tchau, tchau')

    def acessa(self, url, seg=1, path='//*[@id="site-content"]/div[7]/div/div[1]/div/ul/li[1]/div[1]/a/div[2]/div'):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, seg+90).until(EC.element_to_be_clickable((By.XPATH, path)))

            # if seg:
            #     save(f'{url.split("/")[-2:]}', self.driver.page_source)
            # else:     # TODO DATA LAKE save
            #     save(f'{"_".join(url.split("?")[-1:])}', self.driver.page_source)
            return self.driver.page_source

        except TimeoutException:
            print(f'\ncansei de espera\n pagina :{url}\n tempo de espera: {seg+90}\n')
            return None

        except Exception as e:
            print(f'\n MALS AII!! \n {e}')
            self.acessa(url=url, seg=seg, path=path)




