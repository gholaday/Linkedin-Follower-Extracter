from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def GetFollowers():

    names = set()

    url = input('Enter the company name on linkedIn (ex: z1-solutions): ')
    username = input('Enter your linkedin email (must be admin of company to view followers): ')
    password = input('Enter your password: ')
    
    wd = webdriver.Firefox()
    wd.get('https://www.linkedin.com')


    email = wd.find_element_by_id('login-email')
    pword = wd.find_element_by_id('login-password')

    email.send_keys(username)
    pword.send_keys(password)

    #Linkedin has very inconsistent html tags...so we have to check both - otherwise it crashes
    try:
        wd.find_element_by_name("submit").click()
    except:
        wd.find_element_by_id("login-submit").click()

    if wd.current_url != 'https://www.linkedin.com/nhome/':
        print('log-in credentials incorrect!')
        wd.quit()
        return

    try:
        wd.get('https://www.linkedin.com/company/' + url + '/followers?page_num=1')
    except:
        print('Company URL does not exist!')
        wd.quit()
        return

    fn = url + '-names.txt'

    #Keep running, adding names to list and clicking 'next' until you run out of pages
    while True:
        timeout = 0     #should offer a bit of protection against an infinite loop
        while True:
            if timeout == 30:
                print('page timeout - loading took too long\nExiting...')
                return 
            try:
                source = wd.find_element_by_id('content').get_attribute('outerHTML')
                break
            except:
                print('page not loaded - retrying...')
                time.sleep(1)
                timeout += 1
                pass
           

        soup = BeautifulSoup(source, 'xml')

        for name in soup.findAll('p', attrs={'class':'fn n'}):
            names.add(name.find('a').text)
        
        try:
            next = wd.find_element_by_xpath('//*[@id="content"]/div/span/a[text()[contains(.,"next")]]')
            wd.execute_script('window.scrollTo(0, arguments[0]);', next.location['y']-250)
            time.sleep(.5)
            next.click()
        except:
            break

    SaveNames(fn, names)
    wd.quit()

def SaveNames(fileName, names):
    print('Saving to ' + fileName + '...')
    file = open(fileName, 'w')
    for name in names:
        try:
            file.write(name + '\n')
        except:
            pass

    print('File Saved!')
    file.close()
        


GetFollowers()
