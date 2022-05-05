from selenium import webdriver
from json import load
from selenium.common import exceptions
from time import sleep

file_name = "cookies.json"
driver = webdriver.Firefox()

with open(file_name, "r", encoding="UTF-8") as f:
	cookie_dict = load(f)


driver.get(cookie_dict["url"])
for cookie in cookie_dict["cookies"]:
	if cookie["sameSite"] == "unspecified":
		cookie["sameSite"] = "Lax"
	elif cookie["sameSite"] == "no_restriction":
		cookie["sameSite"] = "None"
	else:
		cookie["sameSite"] = "Strict"
	
	driver.add_cookie(cookie)

driver.get_cookies()

# After Auth Get the free game
driver.get("https://www.epicgames.com/store/en-US/free-games")
sleep(4)

try:

	free_now = driver.find_elements_by_xpath("//span[text()='Free Now']")[0]
except exceptions.NoSuchElementException:
	quit("No free game available right now")

driver.execute_script('arguments[0].click()', free_now)
sleep(4)
#18+ game check
try:
	continue_button = driver.find_element_by_xpath("//span[text()='Continue']")
	if continue_button.text == "CONTINUE" : 
		driver.execute_script('arguments[0].click()', continue_button)
	else:
		raise exceptions.NoSuchElementException
except exceptions.NoSuchElementException:
	pass

sleep(4)
add_to_cart = driver.find_elements_by_xpath("//span[text()='Add To Cart']")[0] 
driver.execute_script('arguments[0].click()', add_to_cart)
sleep(4)
driver.get("https://www.epicgames.com/store/en-US/cart")
sleep(4)
check_out = driver.find_elements_by_xpath("//span[text()='Check Out']")[0]
driver.execute_script('arguments[0].click()', check_out)
sleep(10) # Suppppper slow
iframe = driver.find_element_by_xpath("//div[4]/iframe")
driver.switch_to.frame(iframe)
place_order = driver.find_elements_by_xpath("//span[text()='Place Order']")[0]
driver.execute_script('arguments[0].click()', place_order)
sleep(4)

"""
This is the part I gave up, it asks for captcha to claim the freeby. 
although if you don't run it quite agressively. it might not. 	

Lets say it didn't. lets see what's next ?
"""

sleep(4)
if "success" in driver.current_url:
	print("VOILA")
else:
	print("Fucked")