from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep

def row_number():
    # Counts the number of rows in the table on site
    global rows
    rows = 0
    table_rows = driver.find_elements_by_xpath('//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[3]/div/div/div[4]/table/tbody/tr')
    rows = len(table_rows) - 1

def dataframe(rows):
    global df
    for i in range(2, rows + 2): # Adjusted to the structure of the page
        data = driver.find_elements_by_xpath('//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[3]/div/div/div[4]/table/tbody/tr[' + str(i) + ']/td') # Get Table Row Data from Site
        table_data = [element.text for element in data] # Convert to List
        series = pd.Series(table_data, index=df.columns) # Create Series
        df = df.append(series, ignore_index=True) # Append to Dataframe
    df.loc[df.Status == "Failed\nView Details", "Status"] = "Failed" # Rename Failed View Details to Failed
    df.loc[df.Status == "Go", "Status"] = "Pending" # Rename Go field to Pending 

email = input("Input email: ")
password = input("Input password: ")
# ---------------------------------------------------------------------------------------------------------------------

# Setup Chrome Driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # HEADLESS BROWSER
chrome_options.add_argument("--log-level=3") # DON'T SHOW LOGS IN CLI
chrome_driver_binary = r"C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe" # Chrome Driver Location
driver = webdriver.Chrome(executable_path=chrome_driver_binary, options=chrome_options)

# Navigate to KodeKloud Engineer
driver.get('https://www.kodekloud-engineer.com')
driver.implicitly_wait(30)

# Login
username = driver.find_element_by_id("inputEmail").send_keys(email)
password = driver.find_element_by_id("inputPassword").send_keys(password)

sign_in_button = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/form[1]/button[1]").click()
sleep(2)

# Find dropdown menu and choose page size 100
dropdown = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/div[3]/div/div/div[2]/button").click()
sleep(0.5)
dropdown_100 = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/div[3]/div/div/div[2]/div/a[5]").click()
sleep(4.5)

# Scroll to the bottom of the page by executing JS
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# ---------------- Second Part of the Script ------------------------------------------------------------------
# Get the Table Header
header = driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[3]/div/div/div[4]/table/thead/tr').text.split(' ')
table_header = header[:2] + [header[2] + " " + header[3]] + header[-2:] # Same as header just concatenated Due By

# DATAFRAME CREATION FIRST PAGE
df = pd.DataFrame(columns = table_header)

row_number()
dataframe(rows)

# CLICK ON NEXT BUTTON
next = driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[3]/div/div/div[6]/a[2]')
next.click()
sleep(4)

# CHECK IF THERE ARE MORE THAT 100 TASKS
# task_number = driver.find_element_by_xpath('//*[@id="main-wrapper"]/div[3]/div/div/div[1]/div[3]/div/div/div[6]')
# task_number.text.split(' of ')[1].split(' entries ')[0]

# SECOND PAGE
row_number()
dataframe(rows)
print(driver.title)
driver.quit()


# JOIN BASIC AND BONUS EXPERIENCE
#for i in range(len(df)):
#    if len(df.loc[i, 'Experience'].split(' ')) > 1:
#        df.loc[i, 'Experience' ] = int(df.loc[i, 'Experience' ].split(" ")[0]) + int(df.loc[i, 'Experience' ].split(" ")[1])  
#    else:
#        pass


print(df.to_string(), '\n') # Print ALL