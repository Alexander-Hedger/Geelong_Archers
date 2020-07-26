from announcements.models import Announcement
from events.models import EventIntro, EventComp, EventMotD
from accounts.models import Committee
from django.contrib import messages
from django.contrib.auth.models import User

# Scraping requirements
import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from awards.models import MemberEvents, MemberAwards, MemberAvailableAwards, MemberClassification, MemberClassificationAnnual, Awards
from django.shortcuts import redirect
from datetime import date
from selenium.webdriver.chrome.options import Options


def sidebar(request):

    if request.user.is_authenticated:
        announcements = Announcement.objects.order_by(
            '-date_published').filter(is_published=True)[:3]

    else:
        announcements = Announcement.objects.order_by(
            '-date_published').filter(is_published=True, members_only=False)[:3]

    events_motd = EventMotD.objects.order_by(
        'date_start').filter(is_published=True)[:4].values('short_title', 'short_description', 'date_start', 'date_end')
    events_comp = EventComp.objects.order_by(
        'date_start').filter(is_published=True)[:4].values('short_title', 'short_description', 'date_start', 'date_end')
    events_intro = EventIntro.objects.order_by(
        'date_start').filter(is_published=True)[:4].values('short_title', 'short_description', 'date_start', 'date_end')

    query1 = events_motd.union(events_comp)
    query2 = query1.union(events_intro)
    events = query2.order_by('date_start')[:4]

    context = {
        'announcements': announcements,
        'events': events
    }

    return context


def validate():
    come_and_try_id = Committee.objects.get(
        position='Come and Try Coordinator').member.id

    webmaster_id = Committee.objects.get(
        position='Webmaster').member.id

    validate_events_intro = [webmaster_id]
    validate_events_comp = [webmaster_id, come_and_try_id]

    context2 = {
        'validate_events_intro': validate_events_intro,
        'validate_events_comp': validate_events_comp
    }

    return context2


def scrape(request):
    name = str(request.user)

    # Development
    CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    CHROMEDRIVER_PATH = 'static/webdrivers/chromedriver'

    # Production
    # CHROME_PATH = "/usr/bin/google-chrome-stable"
    # CHROMEDRIVER_PATH = 'static/webdrivers/chromedriver'

    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    # Use to run chrome with head display [for debugging]
    driver = webdriver.Chrome(executable_path=(
        'static/webdrivers/chromedriver'))

    # driver = webdriver.Chrome(
    #     executable_path=(CHROMEDRIVER_PATH), chrome_options=chrome_options)

    url = 'https://www.archersdiary.com/MyEvents.aspx'

    driver.get(url)

    name_input = '//*[@id="ctl00_mainContent_txtName"]'

    driver.find_element_by_xpath(name_input).send_keys(name)
    driver.find_element_by_xpath(name_input).send_keys(u'\ue007')

    driver.implicitly_wait(10)
    driver.find_element_by_xpath(
        '//*[@id="ctl00_mainContent_GridView1"]/thead/tr/th[1]')

    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    events = soup.find_all(
        'tr')

    event_history = {}
    count = 0
    award_count = 0

    # Get all new events
    for row in events[1:]:
        cells = row.find_all("td")
        url = cells[0].find('a').get('href')

        if url is not None:

            link = f'https://www.archersdiary.com/{url}'

            # Remove Existing Events
            if MemberEvents.objects.filter(member=request.user, link=link).exists():
                continue

            count += 1

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

            # Clean date format
            date = datetime.strptime(
                date, '%d/%m/%Y').strftime('%Y-%m-%d')

            event_history[link] = {
                'link': link,
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
                'awards': [],
                'total_awards': 0
            }

    # Go through each New event
    for event in event_history.items():

        # Add the 'awards' field onto each Outdoor or Indoor Event item
        if event[1]['discipline'] == 'Outdoor' or event[1]['discipline'] == 'Indoor' or event[1]['discipline'] == 'Clout':

            scorecard_url = event[1]['link']
            response = requests.get(scorecard_url)
            soup = BeautifulSoup(response.text, 'html.parser')

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

                    for row in flight.find_all('tr')[1:-1]:
                        for td in row.find_all('td')[-1:]:
                            award = td.get_text()
                            award = award.replace(' Score', '')
                            if award != u'\xa0' and award != '':
                                # Select the awards array
                                array = event[1]['awards']

                                event[1]['total_awards'] += 1
                                # Create the award name
                                if event[1]['discipline'] == 'Clout' or event[1]['discipline'] == 'Indoor':
                                    award_key = f"{distance} - {award}"
                                else:
                                    award_key = f"{distance} {diameter} - {award}"
                                # Get award sublist if already exists
                                award_check = [
                                    item for item in array if item[0] == award_key]
                                # Check if it exists
                                if award_check:
                                    # if exists add 1 to the count
                                    array[array.index(
                                        award_check[0])][1] += 1
                                else:
                                    array.append([award_key, 1])
                                    award_key_list.append(award_key)

            # With awards field added, Add Event to MemberEvents Model
            new_event = MemberEvents(member=request.user, link=event[1]['link'], event_name=event[1]['event_name'], club=event[1]['club'], discipline=event[1]['discipline'], date=event[1]['date'], day=event[1]['day'],
                                     flight=event[1]['flight'], archer_class=event[1]['archer_class'], division=event[1]['division'], archery_round=event[1]['archery_round'], score=event[1]['score'], rating=event[1]['rating'], awards=event[1]['awards'], total_awards=event[1]['total_awards'])
            new_event.save()

            # Check if awards on new event
            if award_key_list:
                # Remove Duplicate awards from award_key_list
                award_key_list = list(dict.fromkeys(award_key_list))
                for award_key in award_key_list:
                    # Some awards on Archer's Diary dont exist, check if they exist first
                    try:
                        # Get Award ID from Award Model
                        award_id = Awards.objects.get(name=award_key)
                        # check if member already has award, if not, add it.
                        if not MemberAwards.objects.filter(member=request.user, award=award_id).exists():
                            award_count += 1
                            # Add new award to MemberAwards
                            new_member_award = MemberAwards(
                                member=request.user, award=award_id, date_recieved=event[1]['date'])
                            new_member_award.save()
                            # Add new award to MemberAvailableAwards
                            new_member_available = MemberAvailableAwards(
                                member=request.user, award=award_id)
                            new_member_available.save()
                    except Awards.DoesNotExist:
                        pass

        # Add the 'awards' field onto each Field Event item
        elif event[1]['discipline'] == 'Field':
            scorecard_url = event[1]['link']
            response = requests.get(scorecard_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            award_key_list = []

            for table in soup.find_all('table'):
                for flight in table.find_all('table')[1:-1]:
                    for row in flight.find_all('tr')[1:-1]:
                        for td in row.find_all('td')[:1]:
                            target = td.get_text()
                        for td in row.find_all('td')[-1:]:
                            award = td.get_text()
                        if award != u'\xa0' and award != '':
                            # Select the awards array
                            array = event[1]['awards']
                            # Create the award name
                            award_key = f"Target {target} - {award}"
                            # Get award sublist if already exists
                            award_check = [
                                item for item in array if item[0] == award_key]
                            # Check if it exists
                            if award_check:
                                # if exists add 1 to the count
                                array[array.index(
                                    award_check[0])][1] += 1
                            else:
                                array.append([award_key, 1])
                                award_key_list.append(award_key)

            # With awards field added, Add Event to MemberEvents Model
            new_event = MemberEvents(member=request.user, link=event[1]['link'], event_name=event[1]['event_name'], club=event[1]['club'], discipline=event[1]['discipline'], date=event[1]['date'], day=event[1]['day'],
                                     flight=event[1]['flight'], archer_class=event[1]['archer_class'], division=event[1]['division'], archery_round=event[1]['archery_round'], score=event[1]['score'], rating=event[1]['rating'], awards=event[1]['awards'], total_awards=event[1]['total_awards'])
            new_event.save()

    if count > 0 and award_count > 0:
        messages.success(
            request, f'{count} new events have been updated with {award_count} new awards available!')
    elif count > 0:
        messages.success(request, f'{count} new events have been updated!')
    else:
        messages.success(request, 'Your events are up to date!')

    # Get classification
    url = 'https://www.archersdiary.com/ClassificationLookup.aspx'
    driver.get(url)
    driver.find_element_by_xpath(name_input).send_keys(u'\ue007')

    driver.find_element_by_xpath(
        '//*[@id="ctl00_mainContent_Table1"]/tbody/tr[1]/th[1]')

    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    classification_table = soup.find(
        'table', id="ctl00_mainContent_Table1")

    classification_rows = classification_table.find_all('tr')

    classification_history = {}

    for row in classification_rows[1:]:
        cells = row.find_all("td")

        discipline = cells[0].get_text()
        archer_class = cells[1].get_text()
        division = cells[2].get_text()
        classification = cells[3].get_text()
        score_count = cells[4].get_text()

        # clean score_count
        score_count = score_count.replace(' (view)', '')

        key = f'{discipline} {archer_class} {division} - {classification}'

        classification_history[key] = {
            'discipline': discipline,
            'archer_class': archer_class,
            'division': division,
            'classification': classification,
            'score_count': int(score_count),
        }

    classifications = ['White', 'Black', 'Blue', 'Red', 'Gold', 'Master Bowman',
                       'Grand Master Bowman', 'Elite Bronze', 'Elite Silver', 'Elite Gold']

    year = datetime.now().year
    year = int(year)

    # Go through each new record
    for record in classification_history.items():
        key = record[0]
        annual_key = f'{key} {year}'

        discipline = record[1]['discipline']
        archer_class = record[1]['archer_class']
        division = record[1]['division']
        classification = record[1]['classification']
        score_count = record[1]['score_count']
        classification_name = f'{discipline} {classification}'
        classification_id = Awards.objects.get(name=classification_name)

        rank = int(classifications.index(classification))

        # If rank is a normal rank
        if rank < 5:
            try:

                # Get record ID from Award Model
                record_id = MemberClassification.objects.get(name=key)
                record_id.score_count = score_count
                record_id.save()

            except MemberClassification.DoesNotExist:
                new_record = MemberClassification(member=request.user, name=key, rank=rank, discipline=discipline, archer_class=archer_class,
                                                  division=division, classification=classification, score_count=score_count, classification_id=classification_id)
                new_record.save()

        else:
            try:

                # Get record ID from Award Model
                record_id = MemberClassificationAnnual.objects.get(
                    name=annual_key)
                record_id.score_count = score_count
                record_id.save()

            except MemberClassificationAnnual.DoesNotExist:
                new_record = MemberClassificationAnnual(member=request.user, name=annual_key, rank=rank, discipline=discipline, archer_class=archer_class,
                                                        division=division, classification=classification, score_count=score_count, year=year, classification_id=classification_id)
                new_record.save()

    driver.quit()
    return redirect('dashboard')
