# here I'm going to learn how to web scrape for data, and then hopefully this document is well
# organized enough to allow me to do a few experiments below it with web scraping

# oh, also, I'm following beautiful soup's tutorial for static web scraping:
# https://realpython.com/beautiful-soup-web-scraper-python/



"""import requests # this big chunk up here is my first attempt at web scraping - just followed the tutorial
# to a tee (to a t? to a tea? idk but you know what I mean)

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

print(page.text)"""
"""
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id='ResultsContainer')
#print(results.prettify())
job_elements = results.find_all('div',class_='card-content')
"""
"""for job_element in job_elements:
    #print(job_element, end='\n'*2)
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()"""
"""
python_jobs = results.find_all(
    'h2',string=lambda text:'python' in text.lower()
)

#print(python_jobs)

python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

for job_element in python_job_elements:
    #print(job_element, end='\n'*2)
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    #links = job_element.find_all('a')
    #for link in links:
    #    apply = link.text.strip()
    #    if apply == 'Apply':
    #        link_url = link['href']
    #        print(f'Apply here: {link_url}\n')# this was my solution... I feel like it's better but whatever
    link_url = job_element.find_all('a')[1]['href']
    print(f'Apply here: {link_url}\n') # this was their solution...
    # the code is better tbh but mine is better for error checking I think
    print()
"""

# second section where I try it out on indeed.com

import requests
from bs4 import BeautifulSoup
import pandas as pd

search_query = 'economics'#input('Input search query: ')
location = input('Input location: ')
numPages = int(input('How many pages to scrape: '))

data = pd.DataFrame()
data['title'] = ''
data['company'] = ''
data['location'] = ''
data['salary'] = ''
data['rating'] = ''
data['business'] = ''
data['remote'] = ''
data['new'] = ''

title_elements = []
company_elements = []
location_elements = []
#stringSalaries = []
salaries = []
ratings = []
business = []
remote = []
new = []

count = 0

for pageNum in range(numPages):
    URL = 'https://www.indeed.com/jobs?q=' + search_query + '&l=' + location + '&start=' + str(pageNum * 10)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mosaic-provider-jobcards')
    job_elements = soup.find_all('div',class_='job_seen_beacon')

    for job_element in job_elements:
        #print(job_element)
        title = job_element.find('h2',class_='jobTitle').text.strip()
        title_elements.append(title)
        data.loc[count, 'title'] = title
        if 'business' in title or 'Business' in title:
            data.loc[count, 'business'] = 1
        elif 'Business' not in title and 'business' not in title:
            data.loc[count, 'business'] = 0

        company_elements.append(job_element.find('span',class_='companyName').text.strip())
        data.loc[count, 'company'] = job_element.find('span',class_='companyName').text.strip()

        location_elements.append(job_element.find('div',class_='companyLocation').text.strip())
        data.loc[count, 'location'] = job_element.find('div',class_='companyLocation').text.strip()

        salary = job_element.find('span',class_='salary-snippet')
        if salary is not None:
            #stringSalaries.append(salary.text.strip())
            if salary.text.strip().find('hour') != -1:
                if salary.text.strip().find('-') != -1:
                    first_sal = salary.text.strip()[0:salary.text.strip().index('-')]
                    second_sal = salary.text.strip()[salary.text.strip().index('-'):]
                    first_sal_num = ''
                    second_sal_num = ''
                    for char in first_sal:
                        if char.isdigit():
                            first_sal_num += char
                        elif '.' in char:
                            first_sal_num += char
                    for char in second_sal:
                        if char.isdigit():
                            second_sal_num += char
                        elif '.' in char:
                            second_sal_num += char
                    salary_num = float(((float(first_sal_num) + float(second_sal_num)) / 2) * 40.0 * 52.0)
                    salaries.append(salary_num)
                    data.loc[count, 'salary'] = salary_num
                elif salary.text.strip().find('-') == -1:
                    salary_num = ''
                    for char in salary.text.strip():
                        if char.isdigit():
                            salary_num += char
                        elif '.' in char:
                            salary_num += char
                    salary_num = float(float(salary_num) * 40.0 * 52.0)
                    salaries.append(salary_num)
                    data.loc[count, 'salary'] = salary_num
            elif salary.text.strip().find('hour') == -1:
                if salary.text.strip().find('-') != -1:
                    first_sal = salary.text.strip()[0:salary.text.strip().index('-')]
                    second_sal = salary.text.strip()[salary.text.strip().index('-'):]
                    first_sal_num = ''
                    second_sal_num = ''
                    for char in first_sal:
                        if char.isdigit():
                            first_sal_num += char
                        elif '.' in char:
                            first_sal_num += char
                    for char in second_sal:
                        if char.isdigit():
                            second_sal_num += char
                        elif '.' in char:
                            second_sal_num += char
                    salary_num = (float(first_sal_num) + float(second_sal_num)) / 2
                    salaries.append(float(salary_num))
                    data.loc[count, 'salary'] = float(salary_num)
                elif salary.text.strip().find('-') == -1:
                    salary_num = ''
                    for char in salary.text.strip():
                        if char.isdigit():
                            salary_num += char
                        elif '.' in char:
                            salary_num += char
                    salary_num = salary_num
                    salaries.append(float(salary_num))
                    data.loc[count, 'salary'] = float(salary_num)
        elif salary is None:
            #stringSalaries.append('')
            salaries.append('')
            data.loc[count, 'salary'] = ''

        rating = job_element.find('span', class_='ratingsDisplay withRatingLink')
        if rating is not None:
            ratings.append(rating.text.strip())
            data.loc[count, 'rating'] = float(rating.text.strip())
        elif rating is None:
            ratings.append('')
            data.loc[count, 'rating'] = ''

        remote_element = job_element.find('span',class_='remote-bullet')
        if remote_element is not None:
            remote.append(1)
            data.loc[count, 'remote'] = 1
        elif remote_element is None:
            remote.append(0)
            data.loc[count, 'remote'] = 0

        new_element = job_element.find('span',class_='label')
        if new_element is not None:
            new.append(1)
            data.loc[count, 'new'] = 1
        elif new_element is None:
            new.append(0)
            data.loc[count, 'new'] = 0

        count += 1


for title in title_elements:
    if 'Business' in title or 'business' in title:
        business.append(1)
    elif 'Business' not in title and 'business' not in title:
        business.append(0)
"""
print(len(title_elements), title_elements)
print(len(company_elements), company_elements)
print(len(location_elements), location_elements)
print(len(stringSalaries), stringSalaries)
print(len(salaries), salaries)
print(len(ratings), ratings)
print(len(business), business)
print(len(remote), remote)
print(len(new), new)

print()#"""
print(data)

data.to_csv('data.csv',index=False)

#business_jobs = results.find_all(
#    'h2', string=lambda text: "business" in text.lower()
#)

#print(len(business_jobs))

