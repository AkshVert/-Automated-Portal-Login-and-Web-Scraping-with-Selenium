from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class PortalLoginAndScraper:
    def __init__(self, webdriver_path, portal_url, username, password):
        self.webdriver_path = webdriver_path
        self.portal_url = portal_url
        self.username = username
        self.password = password

        # Setup Edge options
        self.edge_options = Options()
        self.edge_options.add_argument("--start-maximized")

        # Initialize WebDriver
        self.service = Service(self.webdriver_path)
        self.driver = webdriver.Edge(service=self.service, options=self.edge_options)

    def login(self):
        try:
            # Open the portal URL
            self.driver.get(self.portal_url)

            # Wait for the username field to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )

            # Locate the username and password fields and enter credentials
            username_field = self.driver.find_element(By.ID, 'email')
            password_field = self.driver.find_element(By.ID, 'password')

            username_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Submit the login form
            password_field.send_keys(Keys.RETURN)

            # Wait for the post-login page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'some-element-after-login'))
            )

            print("Login successful. Proceeding to scrape data...")
            return True

        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def scrape_data(self):
        try:
            # Example: Scraping data from a table after login
            table_rows = self.driver.find_elements(By.XPATH, '//table[@id="data-table"]/tbody/tr')

            data = []
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]
                data.append(row_data)

            # Convert scraped data into a DataFrame
            df = pd.DataFrame(data, columns=['Column1', 'Column2', 'Column3'])  # Adjust columns as per your table
            print(df)

            # Save the scraped data to a CSV file
            df.to_csv('scraped_data.csv', index=False)
            print("Data scraped and saved to 'scraped_data.csv'.")

        except Exception as e:
            print(f"Error during data scraping: {e}")

    def run(self):
        if self.login():
            self.scrape_data()
        self.driver.quit()

if __name__ == "__main__":
    # WebDriver path and portal details
    webdriver_path = # Path to your webdriver where it is stored after extraction
    portal_url = 'https://utl/login'  # Replace with your portal URL
    username = 'email'  # Replace with your username
    password = 'password'  # Replace with your password

    # Create an instance of the automation and scraper class
    scraper = PortalLoginAndScraper(webdriver_path, portal_url, username, password)
    scraper.run()
