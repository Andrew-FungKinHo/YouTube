from tabula.io import read_pdf
import requests,lxml
from bs4 import BeautifulSoup
import urllib3
import smtplib
from email.message import EmailMessage
import os
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path,'test_log.log')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

def do_logging(message):
    logger.info(f'Data Successfully Fetched: Your hall waitlist position is #{message}')


def send_email(position,link):
    EMAIL_ADDRESS = 'ENTER YOUR EMAIL ADDRESS HERE'
    EMAIL_PASSWORD = 'ENTER YOUR EMAIL PASSWORD HERE'

    # New Email Message
    msg = EmailMessage()
    msg['Subject'] = f'Your Hall Waitlist Position is #{position}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'ENTER YOUR DESIGNATED MAILBOX HERE'
    msg.set_content(f'You can find the waitlist PDF via the link: {link}')

    # Send the message
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

def find_waitlist_position():
  MAIN_URL = 'https://shrl-admission.ust.hk/ughwaitinglist'
  BASE_URL = 'https://shrl-admission.ust.hk/'
  PDF_URL = ''
  student_id = 20512970       # RANDOM STUDENT ID
  position = 0

  urllib3.disable_warnings()

  html = requests.get(MAIN_URL,verify=False).text

  soup = BeautifulSoup(html,'lxml')

  textArea = soup.find('div',class_="hkust-simple-text")

  links = textArea.findAll('a',href=True)

  for link in links:
    if '2021' in link['href']:
      PDF_URL = BASE_URL + str(link['href'])

  df = read_pdf(PDF_URL,pages='all',multiple_tables=True)
  # print(df)

  for i in range(len(df)):
    if student_id in df[i][df[i].columns[0]].tolist():
      index = df[i][df[i].columns[0]].tolist().index(student_id)
      position = df[i].iloc[index,1]
      break

  # print(f'Position is: {position}')
  # print(f'Link is: {PDF_URL}')
  return position, PDF_URL

if __name__ == "__main__":
    waitlist_position,link = find_waitlist_position()
    print(f'Position is: {waitlist_position}')
    print(f'Link is: {link}')
    do_logging(waitlist_position)
    send_email(waitlist_position,link)
    print('EMAIL SUCCESSFULLY SENT!')

