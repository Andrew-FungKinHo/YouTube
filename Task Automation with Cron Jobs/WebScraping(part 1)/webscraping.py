from tabula.io import read_pdf
import requests,lxml
from bs4 import BeautifulSoup
import urllib3

def find_waitlist_position():
  MAIN_URL = 'https://shrl-admission.ust.hk/ughwaitinglist'
  BASE_URL = 'https://shrl-admission.ust.hk/'
  PDF_URL = ''
  student_id = 20766105
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
  print(waitlist_position)
  print(link)
