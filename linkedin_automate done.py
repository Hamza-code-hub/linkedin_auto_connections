from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import os

def login(driver, username, password):
    try:
        driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        user.send_keys(username)
        password_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)
        print("Login successful.")
    except TimeoutException:
        print("Timeout while trying to log in.")
    except Exception as e:
        print(f"An error occurred during login: {e}")

def connect_with_profile(driver, profile_url, message=None):
  try:
    driver.get(profile_url)

    # Try finding the direct "Connect" button first
    try:
        connect_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]'))
        )
        connect_button.click()
        connect_dialog = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )

        # If a message is provided, click Add a note and send the message
        if message:
            add_note_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]/span"))
            )
            add_note_button.click()

            message_box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/div[1]/textarea"))
            )
            message_box.send_keys(message)

        # Click the "Send now" button to send the connection request
            send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/button[2]/span"))
            )
            send_button.click()
        else:
            send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]/span"))
            )
            send_button.click()

        print("Connection request sent successfully (direct button).")
        return
    except (TimeoutException, StaleElementReferenceException):
      pass  # Proceed to checking the "More" menu if direct button not found

    # If direct button not found, check for "Follow" button and use "More" menu
    follow_button_present = False
    try:
      follow_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button")))
      follow_button_present = True
    except NoSuchElementException:
      pass

    if follow_button_present:
      # Click "More" button and then "Connect" from the dropdown
      more_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]")))
      more_button.click()

      connect_button = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div/span"))
      )
      connect_button.click()
      connect_dialog = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )

        # If a message is provided, click Add a note and send the message
      if message:
        add_note_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]/span"))
        )
        add_note_button.click()

        message_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/div[1]/textarea"))
            )
        message_box.send_keys(message)

        # Click the "Send now" button to send the connection request
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/button[2]/span"))
        )
        send_button.click()
      else:
        send_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]/span"))
        )
        send_button.click()

      # Continue with sending connection request with message (if provided)
      # ... (rest of your code for handling message and sending request)

    print("Connection request sent successfully (via More menu).")

  except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
    print(f"Error sending connection request: {e}")
  except Exception as e:
    print(f"Unexpected error: {e}")
def like_post(driver, post_url):
    try:
        driver.get(post_url)
        like_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Like')]"))
        )
        like_button.click()
        print("Post liked successfully.")
    except TimeoutException:
        print("Timeout while trying to find the like button.")
    except Exception as e:
        print(f"An error occurred while trying to like the post: {e}")
   

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')

    service = Service("C:\\Program Files (x86)\\Chrome Driver\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    your_username = os.getenv("LINKEDIN_USERNAME", "def73858@gmail.com")
    your_password = os.getenv("LINKEDIN_PASSWORD", "*123456789#")

    print(f"Username: {your_username}")
    print(f"Password: {your_password}")

    if not your_username or not your_password:
        print("Username or password not set.")
    else:
        login(driver, your_username, your_password)

        profile_url = "https://www.linkedin.com/in/s4-ali/"
        message = "Hi, I'm interested in connecting with you on LinkedIn."
        # connect_with_profile(driver, profile_url)
        post_url = "https://www.linkedin.com/posts/s4-ali_flutterdev-workspacegoals-developerlife-activity-7191008336098607105-in99?utm_source=share&utm_medium=member_desktop"  # Replace with the actual post URL
        like_post(driver, post_url)

    driver.quit()
