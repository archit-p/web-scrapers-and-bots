from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
search_url = "http://merinfo.se"

old_fd = open('numbers.csv', 'r')
contents = old_fd.read()
contents = contents.split('\n')
old_fd.close()
contents_copy = contents
i = 0
print(len(contents))
for i in range(len(contents)):
    content = contents[i]
    browser = webdriver.Firefox()
    browser.get(search_url)
    time.sleep(20)

    number = content.split(',')[0]

    search_input = browser.find_element_by_class_name("form-control")
    search_input.send_keys(number)
    search_input.send_keys(Keys.RETURN)

    time.sleep(5)
    org_number = '-'
    leader = '-'
    employees = '-'
    innerHTML = browser.execute_script("return document.body.innerHTML")
    if 'Ingen' not in innerHTML:
        try:
        	print('Writing to file')
        	name = browser.find_element_by_class_name("name")
        	link = name.find_element_by_tag_name("a")
        	link.click()
        	time.sleep(2)
        	company = browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div[2]/div/ul/li[3]/a")
        	company.click()
        	time.sleep(2)

       		innerHTML = browser.execute_script("return document.body.innerHTML")
        	if "James saknar bolagsengagemang." in innerHTML:
            		print("No company details found")
            		leader = name.text
            		employees = '-'
            		org_number = '-'
        	else:
            		company_link = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div[2]/div/div/div/div/div/ul/li/a")
            		company_link.click()

            	table = browser.find_element_by_class_name("details")
            	trs = table.find_elements_by_tag_name("tr")
            	for tr in trs:
                	th = tr.find_element_by_tag_name("th")
                	if 'Org.nummer' in th.text:
                		td = tr.find_element_by_tag_name('td')
                    		org_number = td.text
                	if 'Ledamot' in th.text:
                    		td = tr.find_element_by_tag_name('td')
                    		leader = td.text

            		finance = browser.find_element_by_class_name("finance")
            		trs = finance.find_elements_by_tag_name("tr")
            		i = 0
            		for i in range(len(trs)):
                		if 'Antal' in trs[i].text:
                    			td = trs[i+1].find_element_by_tag_name("td")
                    			employees = td.text
	except:
     		print('Error encountered')
    else:
        print("No details found")
    contents_copy.remove(content)
    old_fd = open("numbers.csv", "w")
    old_fd.write('\n'.join(contents_copy))
    old_fd.close()
    browser.close()
    print('Done')
    print('Writing to file...')
    fd = open('details.csv', 'a+')
    fd.write(content + ',' + org_number + ',' + leader + ',' + employees + '\n')
    fd.close()
print("Done scraping")
