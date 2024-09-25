from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os, time, argparse, json, datetime


output_dir = "dailymirror_archive_pages"
json_dir = "cleaned_data"

# Scrape from the webpage
def scrape_data():
    # Initialize the driver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # Create a directory to save the HTML files if not there
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Go to the archives page
    driver.get("https://www.dailymirror.lk/archives")

    page_number = 1
    while True:
        try:
            driver.implicitly_wait(5)

            # Save the current page's HTML
            page_html = driver.execute_script("return document.body.innerHTML;")
            with open(f"{output_dir}/page_{page_number}.html", "w", encoding="utf-8") as f:
                f.write(page_html)

            print(f"Saved page {page_number}")

            # Try to find the "Next" button and click it
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'last') and text()='Next']")))

            
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)  # Adjust the wait time if necessary for the page to load
            else:
                print("No more pages.")
                break

            # Increment page counter
            page_number += 1

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Close the browser
    driver.quit()

# Clean the html files and put into JSON by day
def html_clean():
    if not os.path.exists(output_dir):
        print("Output directory does not exist cannot clean")
        return
    
    # Create a directory to save the cleaned data
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    # Get the list of HTML files
    files = os.listdir(output_dir)
    print(f"Found {len(files)} files to clean.")

    date_track = None
    buffer = []
    # Loop through the files
    for count, file in enumerate(files):
        with open(f"{output_dir}/{file}", "r", encoding="utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            art_divs = soup.find_all("div", {"class": "col-md-8"})

            # Find article title, date, and summary
            for div in art_divs:
                try:
                    title = div.find("h3").text
                    date = div.find("span", {"class": "gtime"}).text
                    summary = div.find("p", {"class" : "ng-binding"}).text

                    # Find the day of the article
                    date_obj = datetime.datetime.strptime(date, " %Y-%m-%d %H:%M:%S")

                    # Check if the day is new
                    if date_track == None:
                        date_track = date_obj.date()
                    elif date_track != date_obj.date():
                        date_track = date_obj.date()
                        print(f"Day Done: {date_track.strftime('%Y-%m-%d')} - {len(buffer)} articles | Total: {count}/{len(files)}")
                        # Save the buffer to a JSON file
                        with open(f"{json_dir}/{date_track.strftime('%Y-%m-%d')}.json", "w", encoding="utf-8") as f:
                            json.dump(buffer, f, indent=4)
                        buffer = []
                    
                    # Add the article to the buffer
                    buffer.append({
                        "title": title,
                        "date": date,
                        "summary": summary
                    })

                except Exception as e:
                    continue



        

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="A script to scrape or clean data.")
    
    # Add arguments
    parser.add_argument("-scrape", action="store_true", help="Run the scrape function.")
    parser.add_argument("-clean", action="store_true", help="Run the clean function.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Determine which function to run based on the arguments
    if args.scrape:
        scrape_data()
    elif args.clean:
        html_clean()
    else:
        print("No valid argument provided. Use -scrape or -clean.")

if __name__ == "__main__":
    main()