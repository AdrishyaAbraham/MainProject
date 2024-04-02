from django.test import TestCase

# Create your tests here.
from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        # Log in to the website
        username_input = driver.find_element(By.CSS_SELECTOR, '#username')
        username_input.send_keys("ishta@gmail.com")
        password_input = driver.find_element(By.CSS_SELECTOR, '#password')
        password_input.send_keys("STGEORGE")
        submit_button = driver.find_element(By.CSS_SELECTOR, '#submit')
        submit_button.click()
        time.sleep(2)
        print("Signed in successfully")

        # Navigate to the student leave list
        student_dropdown = driver.find_element(By.ID, 'student')
        student_dropdown.click()
        time.sleep(2)
        leave_list_link = driver.find_element(By.ID, 'leave_list')
        leave_list_link.click()
        time.sleep(2)
        print("Navigated to student leave list page")
        
        # Extract the student ID from the sidebar
        student_id_element = driver.find_element(By.CSS_SELECTOR, '.dropdown-content#student p')
        student_id = student_id_element.text
        print("Student ID:", student_id)
        
        # Add further actions using the student ID as needed
        # For example, you can use the student ID to search for specific student details
        
        # Example: Searching for student details using the student ID
        search_input = driver.find_element(By.CSS_SELECTOR, '#search_input')
        search_input.send_keys(student_id)
        search_button = driver.find_element(By.CSS_SELECTOR, '#search_button')
        search_button.click()
        time.sleep(2)
        
        # Example: Asserting that the student details are displayed
        student_details_element = driver.find_element(By.CSS_SELECTOR, '.student-details')
        assert student_id in student_details_element.text, "Student details not found"

        logout_button = driver.find_element(By.CSS_SELECTOR, ".logout-button")        
        logout_button.click()
        time.sleep(2)
        print("Logged out successfully")

    def test_03_schedule_online_class(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

        username_input = driver.find_element(By.CSS_SELECTOR, '#username')
        username_input.send_keys("ishta@gmail.com")
        password_input = driver.find_element(By.CSS_SELECTOR, '#password')
        password_input.send_keys("STGEORGE")
        submit_button = driver.find_element(By.CSS_SELECTOR, '#submit')
        submit_button.click()
        time.sleep(2)
        print("Signed in successfully")

        # Click on the link to schedule online class
        schedule_link = driver.find_element(By.ID, "onlineclass")        
        schedule_link.click()
        time.sleep(2)
        print("Clicked on Schedule Online Class link")

        # Fill out the form to schedule the class
        enrolled_class_dropdown = driver.find_element(By.ID, 'selectclass')
        enrolled_class_dropdown.send_keys("Sisuvakup")  # Replace "Class Name" with the desired class name

        teacher_dropdown = driver.find_element(By.ID, 'teacher')
        teacher_dropdown.send_keys("Ishta")  # Replace "Ishta" with the desired teacher's name

        date_input = driver.find_element(By.ID, 'datePicker')
        date_input.send_keys("23-03-2024")  # Replace "2024-03-25" with the desired date

        time_input = driver.find_element(By.ID, 'timePicker')
        time_input.send_keys("16:00")  # Replace "10:00 AM" with the desired time

        platform_link_input = driver.find_element(By.ID, 'id')
        platform_link_input.send_keys("https://meet.google.com/mcv-mnxf-uan")  # Replace "https://meet.google.com/mcv-mnxf-uan" with the platform link

        # Submit the form to schedule the class
        schedule_button = driver.find_element(By.ID, 'submit')
        schedule_button.click()
        time.sleep(2)
        print("Scheduled online class successfully")

    def test_apply_leave(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

        # Log in to the teacher dashboard
        username_input = driver.find_element(By.CSS_SELECTOR, '#username')
        username_input.send_keys("ishta@gmail.com")
        password_input = driver.find_element(By.CSS_SELECTOR, '#password')
        password_input.send_keys("STGEORGE")
        submit_button = driver.find_element(By.CSS_SELECTOR, '#submit')
        submit_button.click()
        time.sleep(2)
        print("Signed in successfully")

        # Navigate to the apply leave page
        apply_leave_link = driver.find_element(By.XPATH, "//a[contains(text(),'Apply Leave')]")
        apply_leave_link.click()
        time.sleep(2)
        print("Clicked on Apply Leave link")

        # Fill out the leave application form
        
        start_date_input = driver.find_element(By.CSS_SELECTOR, '#id_leave_date')
        start_date_input.send_keys("17-03-2024")  # Replace with the desired start date

        
        reason_input = driver.find_element(By.CSS_SELECTOR, '#id_leave_message')
        reason_input.send_keys("Feeling unwell")  # Replace with the reason for leave

        # Submit the leave application form
        submit_button = driver.find_element(By.ID, 'submit')
        submit_button.click()
        time.sleep(2)
        print("Leave applied successfully")


