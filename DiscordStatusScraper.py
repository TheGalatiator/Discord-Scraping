"""
Simple web scraper that continuously updates a .csv file with the current
status of Discord servers and all its systems

- Luca Galati
"""
from bs4 import BeautifulSoup
from csv import writer
import requests
import time

url = "https://discordstatus.com/"
web_page = requests.get(url)

"""
Webpage request status codes
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses
"""
# print(web_page)

page_content = BeautifulSoup(web_page.content, "html.parser")  # HTML code
sections = page_content.find_all("div", class_="component-container")
history_codes = ["rhznvxg4v7yh", "r3wq1zsx72bz", "354mn7xfxz1h",
                 "3y468xdr1st2"]  # class names has different suffix for history

while (True):
    with open("DiscordStatus.csv", 'w', encoding='utf8', newline='') as file:
        csv_writer = writer(file)
        header = ["System", "Current Status", "Status History (90 days)"]
        csv_writer.writerow(header)

        for (section, code) in zip(sections, history_codes):
            title = section.find("span", class_="name").text.replace('\n', '') \
                .strip()
            status = section.find("span", class_="component-status").text. \
                replace('\n', '').strip()
            history = section.find("div", class_="legend-item-" + code).text. \
                replace('\n', '').strip()
            info = [title, status, history]
            csv_writer.writerow(info)

        t = time.localtime()
        current_time = time.strftime("%I:%M, %D", t)
        print("Updated at " + current_time)
        csv_writer.writerow([])
        csv_writer.writerow(["Last Updated", current_time])

    time.sleep(60)
