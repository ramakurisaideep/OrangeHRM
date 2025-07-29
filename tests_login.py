import time
from selenium import webdriver
import pytest
from selenium.webdriver import Keys
from config.credentials import credentials
from selenium.webdriver.common.by import By
from utils.helpers import take_screenshot

#Get login data
username, password, login_url, dashboard_url = credentials()
#Launch browser setup
@pytest.fixture()
def browser_setup():
    driver=webdriver.Edge()
    driver.get(login_url)
    driver.maximize_window()
    time.sleep(3)
    yield driver
    driver.close()

#TC001--Login with valid credentials
@pytest.mark.order(1)
def test_valid(browser_setup):
   driver=browser_setup
   driver.find_element(By.NAME,"username").send_keys(username) #valid username
   driver.find_element(By.NAME,"password").send_keys(password) #valid password
   driver.find_element(By.XPATH,"//button[@type='submit']").click()
   time.sleep(3)
   actual_url = driver.current_url
   assert actual_url == dashboard_url, "Login failed: User was not redirected to dashboard"
   take_screenshot(driver, "TC001_Valid_Login_Success")  #Take Screenshot


#TC002--Login with invalid username and valid password
@pytest.mark.order(2)
def test_login_with_invalid_username(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys("invalid")  # invalid username
    driver.find_element(By.NAME, "password").send_keys(password)  # valid password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)
    assert driver.current_url==login_url,"User should not redirect with invalid username"
    take_screenshot(driver,"TC002_Invalid_Username_Error")  #Take Screenshot

#TC003--Login with valid username and invalid password
@pytest.mark.order(3)
def test_login_with_invalid_password(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys(username)  # valid username
    driver.find_element(By.NAME, "password").send_keys("invalid")  # invalid password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)
    assert driver.current_url==login_url,"User should not redirect with invalid password"
    take_screenshot(driver,"TC003_Invalid_Password_Error")  #Take Screenshot

#TC004--Login with invalid username & invalid password.
@pytest.mark.order(4)
def test_login_with_invalid(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys("invalid")  # invalid username
    driver.find_element(By.NAME, "password").send_keys("invalid")  # invalid password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)
    err_msg=driver.find_element(By.XPATH,"//p[text()='Invalid credentials']")
    assert err_msg.text=="Invalid credentials","Error message not displayed."
    take_screenshot(driver,"TC004_Invalid_Credentials_Error")  #Take Screenshot

#TC005--Login with blank username & valid password.
@pytest.mark.order(5)
def test_login_with_blank_username(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys("")  # blank username
    driver.find_element(By.NAME, "password").send_keys(password)  # valid password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(4)
    validation_msg=driver.find_element(By.XPATH,"//span[text()='Required']")
    assert validation_msg.text == "Required", "Validation not displayed."
    take_screenshot(driver,"TC005_Blank_Username_Validation")  #Take Screenshot

#TC006--Login with valid username & blank password.
@pytest.mark.order(6)
def test_login_with_blank_password(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys(username)  # valid username
    driver.find_element(By.NAME, "password").send_keys("")  # blank password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(4)
    validation_msg=driver.find_element(By.XPATH,"//span[text()='Required']")
    assert validation_msg.text == "Required", "Validation not displayed."
    take_screenshot(driver,"TC006_Blank_Password_Validation")  #Take Screenshot

#TC007--Login with blank username & blank password.
@pytest.mark.order(7)
def test_login_with_blank_username_password(browser_setup):
    driver=browser_setup
    driver.find_element(By.NAME, "username").send_keys("")  # blank username
    driver.find_element(By.NAME, "password").send_keys("")  # blank password
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(4)
    validation_msg=driver.find_elements(By.XPATH,"//span[text()='Required']")
    assert len(validation_msg)  == 2, "Validations not displayed."
    take_screenshot(driver,"TC007_Blank_Username_Password_Validation")  #Take Screenshot


# TC009--Verify OrangeHRM Logo
@pytest.mark.order(8)
def test_logo_in_new_tab(browser_setup):
    driver = browser_setup
    # Locate the logo element and get its 'src' attribute
    logo = driver.find_element(By.XPATH, "//img[@alt='company-branding']")
    logo_src = logo.get_attribute("src")
    # Open the logo URL in a new tab
    driver.execute_script(f"window.open('{logo_src}', '_blank');")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    take_screenshot(driver, "TC009_Logo_Screenshot") #Take Screenshot
    # Close the logo tab and switch back to the login page
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

#TC010--Login with valid credentials and print title
@pytest.mark.order(9)
def test_valid_login(browser_setup):
    driver = browser_setup
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    print("Page Title After Login:", driver.title)      # Print page title
    assert driver.current_url == dashboard_url, "Login failed - URL mismatch"
    take_screenshot(driver, "TC010_Login_Page_Title")

#TC011--Verify ENTER key submits the login form
@pytest.mark.order(10)
def test_enter_key(browser_setup):
   driver=browser_setup
   driver.find_element(By.NAME,"username").send_keys(username) #valid username
   # valid password and press ENTER key to submit
   driver.find_element(By.NAME,"password").send_keys(password + Keys.ENTER)
   time.sleep(3)
   actual_url = driver.current_url
   assert actual_url == dashboard_url, "Login failed with ENTER key"
   take_screenshot(driver, "TC011_Enter_Key_Login_Submit")  #Take Screenshot

#TC012--Verify forgot password link navigates
@pytest.mark.order(11)
def test_forgotpassword(browser_setup):
    driver=browser_setup
    driver.find_element(By.XPATH,"//p[text()='Forgot your password? ']").click()
    time.sleep(4)
    exp_url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/requestPasswordResetCode"
    assert exp_url==driver.current_url,"Failed to navigate to Forgot_Password page"
    take_screenshot(driver,"TC012_Forgot_Password")

#TC013--Verify user can log in after resetting the password via "Forgot your password?" link
@pytest.mark.order(12)
def test_login_after_password_reset(browser_setup):
    driver=browser_setup
    driver.find_element(By.XPATH,"//p[text()='Forgot your password? ']").click()
    time.sleep(2)
    driver.find_element(By.NAME,"username").send_keys("Saideep")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    take_screenshot(driver,"TC013_Forgot_Password")

#TC014--Verify "Cancel" redirects to Login page
@pytest.mark.order(13)
def test_verify_cancel(browser_setup):
    driver=browser_setup
    driver.find_element(By.XPATH, "//p[text()='Forgot your password? ']").click()
    time.sleep(2)
    #Click on the cancel button to get redirect to login page.
    driver.find_element(By.XPATH,"//button[@type='button']").click()
    time.sleep(2)
    assert driver.current_url==login_url,"Failed to navigate login page."
    take_screenshot(driver,"TC014_Verify_cancel_button")

#TC015--Reset fails with blank username
@pytest.mark.order(14)
def test_reset_with_blank_username(browser_setup):
    driver=browser_setup
    driver.find_element(By.XPATH, "//p[text()='Forgot your password? ']").click()
    time.sleep(2)
    driver.find_element(By.NAME,"username").send_keys(""+Keys.ENTER) #blank username
    validation_msg=driver.find_element(By.XPATH,"//span[text()='Required']")
    assert validation_msg.text=='Required',"Validation failed."
    take_screenshot(driver,"TC015_Resetbtn")

#TC016--Verify TAB key navigates between login fields
@pytest.mark.order(15)
def test_tab_navigation_between_fields(browser_setup):
    driver=browser_setup
    username_input=driver.find_element(By.NAME,"username")
    password_input=driver.find_element(By.NAME,"password")
    loginbtn=driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys(username + Keys.TAB)
    time.sleep(1)
    active_element=driver.switch_to.active_element
    take_screenshot(driver, "TC016_TAB_Key(1)")
    active_element.send_keys(Keys.TAB)
    active_element=driver.switch_to.active_element
    assert active_element==loginbtn,"TAB Key did not move to focus to password_input."
    take_screenshot(driver,"TC016_TAB_Key(2)")

##TC017--Test loginurl on multiple browsers
@pytest.mark.order(16)
@pytest.mark.parametrize("browser",['chrome','Edge'])
def test_login_cross_browser(browser):
    if browser=='chrome':
        driver=webdriver.Chrome()
    elif browser=='Edge':
        driver=webdriver.Edge()
    else:print("Unsupported browser")
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(3)
    take_screenshot(driver,f"TC017_{browser}.png")
    driver.quit()




