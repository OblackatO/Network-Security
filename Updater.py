from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from typing import List



"""
Updates Websites to be black listen by OpenDNS using a provided list, see main(). 
Note that it would be hard to simply do this with requests lib, or other similar lib. That is why
selenium + phantonjs are used
"""


OPENDNS_LOGIN_PAGE = "https://login.opendns.com/"
driver = webdriver.PhantomJS()
wait = WebDriverWait(driver, 3)

def LoadList(list_path: List[str] = None) -> List[str]:
    """

    :rtype: List[str]: List with all links to be black listed.
    :param: list_path:(List[str],optional) Path to txt
	    files with links to be black listed by OpenDNS.
    """
    all_links = []
    for file_path in list_path:
        with open(file_path, 'r') as links:
            for link in links.readlines():
                all_links.append(link)
    return all_links

def Login(username:str, password:str)->bool:
    """

    :param: username:(str) OpenDNS account name.
    :param: password:(str) OpenDNS password.
    :rtype: bool: True if login successful.
    """
    driver.get(OPENDNS_LOGIN_PAGE)
    driver.page_source()
    username_form = wait.until(ec.presence_of_element_located((By.ID, 'username')))
    username_form.send_keys(username)
    password_form = driver.find_element_by_id('password')
    password_form.send_keys(password, Keys.ENTER)
    #time.sleep(6)
    #driver.save_screenshot("successfullogin_screenshot.png")
    return True

def ClickSettings():
    settings_button_ref = "https://dashboard.opendns.com/settings/"
    settings_button_xpath = '//a[@href="'+settings_button_ref+'"]'
    settings_button = wait.until(ec.presence_of_element_located((By.XPATH, settings_button_xpath)))
    settings_button.click()
    #time.sleep(2)
    #driver.save_screenshot("settings_tab_confirm.png")

def ClickOnNetwork():
    id = "cb142672216"
    network = wait.until(ec.presence_of_element_located((By.ID, id)))
    network.click()
    #time.sleep(2)
    #driver.save_screenshot("network_tab_confirm.png")

def AddBlockDomain(domain_link:str):
    """

    :param: domain_link:(str) Domain to be black listed.
    """
    if "#" in domain_link:
        return
    print("Domain to be added:", domain_link)
    domain_link = domain_link.strip("www.")
    #driver.save_screenshot("Before.png")
    driver.refresh()
    id = "block-domain"
    text_field = wait.until(ec.presence_of_element_located((By.ID, id)))
    text_field.send_keys(domain_link, Keys.ENTER)
    try:
        confirm_button = wait.until(ec.element_to_be_clickable((By.ID, 'confirm-add-domain')))
        confirm_button.click()
    except ElementNotVisibleException:
        pass
    except TimeoutException:
        pass

print("Starting")
password = getpass.getpass("password")
Login("username", password)
ClickSettings()
ClickOnNetwork()
for link in LoadList(['test_file1.txt', 'test_file2.txt']):
    AddBlockDomain(link)
print("Done")

