from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import os

directory = "%s/" % os.getcwd()
file_name = "screenshot.png"

@pytest.fixture
def device(request):
    udid = request.config.getoption("--udid")
    DEVICE = {"name": "current_device", "udid": udid, "appium_port": "4723"}
    return DEVICE
    
@pytest.fixture
def driver(device):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = device["name"]
    options.udid = device["udid"]
    options.app_package = "com.innowireless.xcal.mobile5"
    options.app_activity = "com.innowireless.xcal.mobile5.ui.Main_Activity"
    options.language = "ko"
    options.locale = "KR"
    options.auto_grant_permissions = True
    options.no_reset = True
    options.native_web_screenshot = True
    options.new_command_timeout = 3600

    # 각 디바이스별 스크린샷 파일명 구분
    global file_name
    file_name = f"screenshot_{device['name']}.png"

    driver = webdriver.Remote(
        f"http://127.0.0.1:{device['appium_port']}", options=options
    )

    try:
        yield driver
    finally:
        driver.quit()




def wait_and_find_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )

def wait_and_click_element(driver, locator, timeout=10):
    element = wait_and_find_element(driver, locator, timeout)
    element.click()
    return element

def perform_horizontal_swipe(driver, percentage=0.8):
    deviceSize = driver.get_window_size()
    screenWidth = deviceSize["width"]
    screenHeight = deviceSize["height"]

    start_x = screenWidth * 0.9
    end_x = screenWidth * 0.1
    start_y = screenHeight * 0.2

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(
        driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, start_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def verify_view_title(driver, expected_title, timeout=5):
    title_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().resourceId("com.innowireless.xcal.mobile5:id/tvRfMainViewTitle").text("{expected_title}")'
    )
    return wait_and_find_element(driver, title_locator, timeout)


def test_ui1_loading_check(driver):
    permission_el = WebDriverWait(driver, 205).until(
        EC.presence_of_element_located(
            (
                AppiumBy.ID,
                "com.innowireless.xcal.mobile5:id/tvIntroPermission"
            )
        )
    )
    driver.save_screenshot(directory + file_name)
    print(permission_el.text)
    assert (
        permission_el.text == "Permissions OK."
    ), f"Text mismatch: Expected 'Permissions OK.', but found '{permission_el.text}'"


def test_ui2_find_setting(driver):
    wait_and_click_element(driver, (
        AppiumBy.ID,
        "com.innowireless.xcal.mobile5:id/btnRightSetting"
    ),30)

    wait_and_click_element(driver, (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.innowireless.xcal.mobile5:id/smenu_main_item_text").text("RF View")'
    ),10)

    wait_and_click_element(driver, (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.innowireless.xcal.mobile5:id/tvChild").text("LTE Summary")'
    ),10)

    if verify_view_title(driver, "LTE Summary"):
        perform_horizontal_swipe(driver)
        driver.save_screenshot(directory + file_name)
    

    if verify_view_title(driver, "LTE CA View"):
        perform_horizontal_swipe(driver)
        driver.save_screenshot(directory + file_name)
