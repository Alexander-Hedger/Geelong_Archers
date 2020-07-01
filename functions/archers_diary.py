import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


url = 'https://www.archersdiary.com/MyEvents.aspx'
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url)

name_input = '//*[@id="ctl00_mainContent_txtName"]'

driver.find_element_by_xpath(name_input).send_keys('Ron Noorderbroek')
driver.find_element_by_xpath(name_input).send_keys(u'\ue007')

time.sleep(10)
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

events = soup.find_all(
    'tr', onmouseout="this.style.backgroundColor='White'")

event_history = {}

for row in events:
    cells = row.find_all("td")
    link = cells[0].find('a').get('href')
    event_name = cells[0].get_text()
    club = cells[1].get_text()
    discipline = cells[2].get_text()
    date = cells[3].get_text()
    day = cells[4].get_text()
    flight = cells[5].get_text()
    archer_class = cells[6].get_text()
    division = cells[7].get_text()
    archery_round = cells[8].get_text()
    score = cells[9].get_text()
    rating = cells[10].get_text()

    if link is not None:
        event_history[link] = {

            'link': 'https://www.archersdiary.com/' + link,
            'event_name': event_name,
            'club': club,
            'discipline': discipline,
            'date': date,
            'day': int(day),
            'flight': int(flight),
            'archer_class': archer_class,
            'division': division,
            'archery_round': archery_round,
            'score': int(score),
            'rating': float(rating),
            'awards': []
        }

outdoor_awards = []
field_awards = []
for event in event_history.items():

    if event[1]['discipline'] == 'Outdoor' or event[1]['discipline'] == 'indoor':

        scorecard_url = event[1]['link']
        request = requests.get(scorecard_url)
        soup = BeautifulSoup(request.text, 'html.parser')

        award_key_list = []

        for table in soup.find_all('table'):
            for flight in table.find_all('table')[1:-1]:
                header = flight.find('tr')

                # Get Distance for Award
                distance = header.find('td').get_text()
                distance = distance.replace('Distance: ', '')

                # Get Size of Target Face for Award
                diameter = header.find_all('td')[1].get_text()
                diameter = diameter.replace('WA ', '')

                for row in flight.find_all('tr')[1:6]:
                    for td in row.find_all('td')[-1:]:
                        award = td.get_text()
                        award = award.replace(' Score', '')
                        if award != u'\xa0' and award != '':
                            # Select the awards array
                            array = event[1]['awards']
                            # Create the award name
                            award_key = f"{distance} {diameter} - {award}"
                            # Get award sublist if already exists
                            award_check = [
                                item for item in array if item[0] == award_key]
                            # Check if it exists
                            if award_check:
                                # if exists add 1 to the count
                                array[array.index(award_check[0])][1] += 1
                            else:
                                array.append([award_key, 1])
                                award_key_list.append(award_key)

        print(event[1])

        award_key_list = list(dict.fromkeys(award_key_list))

        for award in award_key_list:
            if award in outdoor_awards:
                pass
            else:
                outdoor_awards.append(award)

    elif event[1]['discipline'] == 'Field':
        scorecard_url = event[1]['link']
        request = requests.get(scorecard_url)
        soup = BeautifulSoup(request.text, 'html.parser')

        awards = []
        for table in soup.find_all('table'):
            for flight in table.find_all('table')[1:-1]:
                for row in flight.find_all('tr')[1:25]:
                    for td in row.find_all('td')[:1]:
                        target = td.get_text()
                    for td in row.find_all('td')[-1:]:
                        award = td.get_text()
                    if award != u'\xa0' and award != '':
                        awards.append(f"Target {target} - {award}")

        awards = list(dict.fromkeys(awards))

        for award in awards:
            if award in field_awards:
                pass
            else:
                field_awards.append(award)

print(outdoor_awards)
print(field_awards)
