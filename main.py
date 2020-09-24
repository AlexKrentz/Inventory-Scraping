import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def site_login():
    pass


def get_out_of_stock_items():
    pass

# a collection of all the product pages we will scrape
url_collection = {
    "cleaning_and_laundry": "https://www.melaleuca.com/ProductStore/content/category?c=52",
    "home_fragrances": "https://www.melaleuca.com/ProductStore/content/category?c=44",
    "vitamins_and_supplements": "https://www.melaleuca.com/ProductStore/content/category?c=2",
    "food_and_weight": "https://www.melaleuca.com/ProductStore/content/category?c=2",
    "medicine": "https://www.melaleuca.com/ProductStore/content/category?c=61",
    "seibella": "https://www.melaleuca.com/ProductStore/content/category?c=30",
    "bath_and_body": "https://www.melaleuca.com/ProductStore/content/category?c=71",
    "oils": "https://www.melaleuca.com/ProductStore/content/category?c=226",
    "logo_gear": "https://www.melaleuca.com/ProductStore/content/category?c=94"
}

open('out_of_stock.html', 'w').close()
f = open("out_of_stock.html", "a")
f.write("""<html>
<head>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}
.parallax {
  /* The image used */

  /* Create the parallax scrolling effect */
  background-position: center;
  background-repeat: repeat-y;
  background-color: #f2f2f2;
  background-size: cover;
}

th, td {
  text-align: left;
  padding: 8px;
}
.big {font-size: x-large;}
.center {text-align: center;}
tr:nth-child(even) {background-color: white;}
</style></head>
<body class="parallax">
<h1 class="center"> Out of Stock Items</h1>
<table>
    <tr class="big" style="background-color:#ccccb3;">
    <th>Product Name</th>
    <th>SKU</th>
    <th>Status</th>
    </tr>""")


# Melaleuca login
def site_login():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "btnSignIn")))
    time.sleep(1)
    browser.find_element_by_id("btnSignIn").click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "UserName")))
    time.sleep(.5)
    browser.find_element_by_id("UserName").send_keys("testus")
    browser.find_element_by_id("Password").send_keys("testpass")
    browser.find_element_by_id("btnSignin").click()

# loop though the dictionary of URLs and scrape
# for out of stock items in each of them

def get_out_of_stock_items():
    for url in url_collection:
        browser.get(url_collection[url])
        # wait for the page to load and see the "show all" button before we attempt to click it
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Show All']")))
        try:
            browser.find_element_by_xpath("//button[text()='Show All']").click()
        except:
            pass
        time.sleep(.5)  # a little buffer after the element is found to ensure no crash
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Temporarily Unavailable')]")))
        except:
            pass
        time.sleep(.5)
        try:
            find_unavailable = browser.find_elements_by_xpath("//*[contains(text(), 'Temporarily Unavailable')]")
        except:
            pass
        try:
            find_discontinued = browser.find_elements_by_xpath("//*[contains(text(), 'Discontinued')]")
        except:
            pass
        try:
            find_available_later = browser.find_elements_by_xpath("//*[contains(text(), 'Available mid')]")
        except:
            pass
        try:
            find_sold_out = browser.find_elements_by_xpath("//*[contains(text(), 'Sold Out')]")
        except:
            pass
        find_unavailable.extend(find_discontinued)
        find_unavailable.extend(find_available_later)
        find_unavailable.extend(find_sold_out)

        for status in find_unavailable:
            if status.text:
                try:
                    name_of_product = status.find_element_by_xpath("../..//h2[@class='product-card__title product-card__copy--heavy ng-binding']")
                    sku = status.find_elements_by_xpath("../..//child::dl[2]//child::dd[1]")
                    f.write("<tr>")
                except:
                    pass
                try:
                    f.write("<td>" + name_of_product.text + "</td> \n")
                except:
                    pass
                try:
                    f.write("<td>" + sku[0].text + "</td><td style=\"color:red\">" + status.text + "</td></tr> \n")
                except:
                    pass
    f.write("</table></body> \n </html>")


path = "C:\\Users\\Alex Krentz\\PycharmProjects\money\\chromedriver.exe"
home_url = "https://www.melaleuca.com/Home"
chrome_options = Options()
chrome_options.add_argument('disable_infobars')
browser = webdriver.Chrome(options=chrome_options)
browser.get(home_url)
site_login()
get_out_of_stock_items()
browser.close()


