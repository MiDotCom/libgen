# Uploads ebooks on Libgen using Python and Selenium
# Searches for ebooks in the book folder, uploads them
# Very important - fills the upload form using the 'file metadata'; so make sure to upload properly tagged file. If needed treat the files Using the Calibre.
# Requirement : selenium (pip install selenium)
# Requirement : chromedriver (download it from : - https://sites.google.com/a/chromium.org/chromedriver/downloads).
# Expects Libgen site to be functioning well at the time of running this script. WebDriverWait components haven't been added. Adding it wouldnt matter anyways if the site is too slow.
# The script has been tested with over 200 ebooks so far. Every error was tackled. If it still gives some error please report it to here, https://github.com/MiDotCom/libgen/issues


import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("") # Change me with Chromedriver path
ext = '.epub', '.pdf', '.mobi', '.azw3' # Change me (if needed); add more supported extensions
lan = 'English' # Change me
folder = "" # Folder containing ebooks; double backslash needed for some system e.g. "C:\\Users\\Ebooks"


def book_folder(path):
	for root, dirs, files in os.walk(path):

		for name in files:
			if name.endswith(ext):
				driver.get("https://genesis:upload@libgen.is/librarian/") # Default Uploader's login:pass info
				try:
					gtwy_error = driver.find_element_by_xpath('/html/body/center[1]/h1') # to handle gatway error after login
					while gtwy_error:
						driver.refresh()
				except:
					pass

				filepath = os.path.join(root, name)
				print("Trying to upload: {} ".format(name))

				driver.find_element_by_xpath('//*[@id="datei1"]').send_keys(filepath)

				driver.find_element_by_xpath('//*[@id="upload_form"]/input[6]').click()
				time.sleep(2)

				# match with current status of upload on Libgen, does nothing if dupe is found
				try:
					status = driver.find_element_by_xpath('/html/body/form[1]/font').text
					if status == 'Editing an existing record':
						print('"{}" already exists on Libgen server.\n'.format(name))
						continue
					elif status == 'Add a new book':
						driver.find_element_by_xpath('/html/body/form[1]/table/tbody/tr[3]/td[3]/input').click()
						time.sleep(2)
						driver.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[7]/td[2]/input').click()
						driver.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[7]/td[2]/input').clear()
						driver.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[7]/td[2]/input').send_keys(lan)
						driver.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[23]/td/input').click()
						time.sleep(5)
				except:
					pass

				# gateway error
				try:
					gtwy_error = driver.find_element_by_xpath('/html/body/center[1]/h1')
					if gtwy_error:
						driver.send_keys(Keys.BACKSPACE)
					else:
						pass
				except:
					pass

				# checking double; a common scenario
				try:
					driver.find_element_by_name('DoublesCheck').click()
					time.sleep(5)
				except:
					pass

				# checking dupe
				try:
					f = driver.find_element_by_xpath('/html/body/h4/a[1]/text()')
					if f:
						continue
					else:
						pass
				except:
					pass

				# final step
				try:
					upload_complete = driver.find_element_by_xpath('/html/body/font/h1').text
					if upload_complete == 'Upload book complete!':
						print("Upload Finished\n\n")
					else:
						pass
				except:
					pass



book_folder(folder)
print("\n\nAll Done")