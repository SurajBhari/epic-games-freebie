from selenium import webdriver
from json import load
from selenium.common import exceptions
from time import sleep

file_name = "cookies.json"
executable_path = r"/home/ag/cookies/geckodriver"
driver = webdriver.Firefox(executable_path=executable_path)

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

free_now =driver.find_element_by_xpath("//div[1]/div/div[4]/main/div[3]/div/div/div/div/div[2]/span/div/div/section/div/div[1]/div/div/a/div/div/div[1]/div[2]/span")
if not free_now.text == "FREE NOW":
	quit("No free game available right now")

free_now.click()
sleep(4)
#18+ game check
try:
	continue_button = driver.find_element_by_xpath("//div[1]/div/div[4]/main/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/button") 
	if continue_button.text == "CONTINUE" : 
		continue_button.click()
	else:
		raise exceptions.NoSuchElementException
except exceptions.NoSuchElementException:
	pass

sleep(4)
add_to_cart = driver.find_element_by_xpath("//div[1]/div/div[4]/main/div[2]/div/div/div/div[2]/div[3]/div/aside/div/div/div[6]/div/button")
add_to_cart.click()
sleep(4)
driver.get("https://www.epicgames.com/store/en-US/cart")
sleep(4)
check_out = driver.find_element_by_xpath("//div[1]/div/div[4]/main/div[2]/div/div/div/div/section/div/div[3]/div[2]/div/div[6]/button")
check_out.click()
sleep(10) # Suppppper slow
iframe = driver.find_element_by_xpath("//div[4]/iframe")
driver.switch_to.frame(iframe)
place_order = driver.find_element_by_xpath("//div[1]/div/div[4]/div/div/div/div[2]/div[2]/button/div/div/span")
place_order.click()
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