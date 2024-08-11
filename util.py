from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from tkinter import simpledialog


def ask_for_url():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user for a URL
    url = simpledialog.askstring("Input", "Please enter the URL:")

    # Close the window
    root.destroy()

    return url


def wait_for_page_load_and_ajax(driver, timeout=30):
    # Wait for the document ready state to be 'complete'
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Check if jQuery is defined, and if so, wait for all jQuery AJAX requests to complete
    jquery_defined = driver.execute_script(
        'return typeof jQuery !== "undefined";')
    if jquery_defined:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return jQuery.active == 0')
        )

    # Optionally, you can also wait for any active XMLHttpRequest requests to complete
    # WebDriverWait(driver, timeout).until(
    #     lambda d: d.execute_script(
    #         'return (window.XMLHttpRequest && XMLHttpRequest.prototype.open.toString().indexOf("native code") === -1) ? 0 : window.XMLHttpRequest.active == 0;')
    # )

        # Example usage:
        # driver = webdriver.Chrome()
        # driver.get("https://example.com")

        # Wait for the page to fully load and AJAX requests to complete
        # wait_for_page_load_and_ajax(driver)

        # Now you can proceed with interacting with the page
