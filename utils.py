from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from File_Class import *
import requests
import shutil
import os
from unidecode import unidecode

def download_img_google(keyword,limit,tryagain):
	options = webdriver.ChromeOptions()
	driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
	list_link = []
	Y = 500
	count = 1
	check = 0
	keyword_search = keyword.replace(' ','+')
	url = f'https://www.google.com/search?q={keyword_search}&tbm=isch'
	driver.get(url)

	WebDriverWait(driver , 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[jsname="sTFXNd"]'))) 
	while True:
		js = '''return len_img = document.querySelectorAll('a[jsname="sTFXNd"]').length'''
		len_img = driver.execute_script(js)
		temp_len = len_img
		for i in range(len_img):
			try:
				js_click = f'''document.querySelectorAll('a[jsname="sTFXNd"]')[{i}].click()'''
				driver.execute_script(js_click)
				js_href = f'''return link = document.querySelectorAll('a[jsname="sTFXNd"]')[{i}].href'''
				link = driver.execute_script(js_href)
				if link not in list_link:
					list_link.append(link)
					if len(list_link) >= limit:
						break
					print(len(list_link))
					count = 0
				else:
					count += 1
					pass
			except:
				pass
		if len(list_link) >= limit or count == 50:
			break
		if temp_len == len_img:
			check += 1
		else:
			check = 0
		if check == 5:
			break
		js_scroll = f'window.scroll(0,{Y})'
		driver.execute_script(js_scroll)
		Y += 200

	if len(list_link) != 0:
		new = ''
		for item in keyword:
			if item == ' ':
				new = new + item
				continue
			else:
				if item.isalnum():
					new = new + item
		name = unidecode(new).strip()
		folder_path = f'./image/{name}'
		temp_file = 1
		while True:
			if os.path.exists(folder_path):
				folder_path = f'./image/{name}-{temp_file}'
				temp_file += 1
			else:
				temp_file = 1
				os.mkdir(folder_path)
				break
		
		list_link_img = [list_link]
		for i in range(len(list_link)):
			driver.get(list_link[i])
			WebDriverWait(driver , 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[id="imi"]'))) 
			js = '''return document.querySelectorAll('img[id="imi"]')[0].src'''
			link_img = driver.execute_script(js)
			list_link_img.append(link_img)

		for i in range(0,len(list_link_img)):
				file_nb = 1
				path_image = folder_path + f"/{unidecode(new).replace(' ','-')}-{i-1}.jpg"
				for j in range(tryagain):
					try:
						response = requests.get(list_link_img[i], stream=True,timeout= 10)
						with open(path_image, 'wb') as out_file:
							shutil.copyfileobj(response.raw, out_file)
						del response
						break
					except:
						continue
	driver.quit()