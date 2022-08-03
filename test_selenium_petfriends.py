from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./chromedriver.exe')
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():

   pytest.driver.find_element_by_id('email').send_keys('kateryna21121996@gmail.com')

   pytest.driver.find_element_by_id('pass').send_keys('123456')

   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


   images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   names = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

def test_my_pets(driver_friends):
      driver_friends.implicitly_wait(10)
      time.sleep(5)
      driver_friends.find_element_by_xpath('//body/nav/div[1]/ul/li[1]/a').click()
      driver_friends.implicitly_wait(10)
      # time.sleep(5)
      assert driver_friends.find_element_by_xpath('//body/div[1]/div/div[1]/h2').text == "Katerina03"
      driver_friends.close()

   img = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/th')))
   pets_photo = 0
   if img[element].get_attribute('src') != '':
      pets_photo += 1
   count_img = len(images)
   assert pets_photo == count_img