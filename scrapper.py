import selenium
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

# setup
username = r"Type_Your_Username"
password = r"Type_Your_Password"
contest_link = r"Contest_Link"

driver = webdriver.Chrome(ChromeDriverManager().install())
search_url = "https://www.hackerrank.com/auth/login"
driver.maximize_window()
driver.get(search_url)

time.sleep(3)
driver.find_element_by_id("input-1").send_keys(username)
driver.find_element_by_id("input-2").send_keys(password)
button = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/form/div[4]/button")
button.click()


driver.get(contest_link)
time.sleep(3)
b = driver.find_element_by_xpath(r"/html/body/div[2]/div[10]/div/div[2]/div/div[3]/div/div[2]/div[1]/ul/li[3]")
b.click()
time.sleep(5)
source_html = bs(driver.page_source, "html.parser")

pages = source_html.find_all('div',{"class":"pagination"})[0].find_all('ul')[0].find_all('li')
pages_list = pages[2:-2]

total_prob = 0
comp_prob = 0

for page in pages_list:
    page_link = "https://www.hackerrank.com/contests" + page.a['href']
    driver.get(page_link)
    time.sleep(3)
    page_source = bs(driver.page_source, "html.parser")
    challenge_list = page_source.find_all('div', {'class': "challenges-list"})[0].find_all('div', {
        "class": "challenges-list-view mdB"})
    total_prob += len(challenge_list)
    for problem in challenge_list:
        yes = problem.div.div.find('div', {"class": "completed-indicator"})
        if (yes != None):
            comp_prob += 1
driver.close()
print("Incomplete Problems: ", end="")
print(total_prob - comp_prob)
