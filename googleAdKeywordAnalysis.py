import requests, lxml, json, time, tldextract
from bs4 import BeautifulSoup

# Specify User Agent 
headers = {
"User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}

listOfKeywords = ["nft","crypto","bitcoin"]
numberOfTimes = 10
resultDict = {}

for keyword in listOfKeywords:
  companyList = []
  numOfTopAds = 0
  numOfBottomAds = 0
  resultDict[keyword] = {}
  absolute_top = 0 
  print(keyword)
  for _ in range(numberOfTimes):
    payload = {'q': keyword}
    html = requests.get("https://www.google.com/search?q=",params=payload,headers=headers)
    status_code = html.status_code

    if status_code == 200:
      response = html.text
      soup = BeautifulSoup(response, 'lxml')
      print('----------------Top Ads-------------------')
      topAds = soup.find(id='tvcap')
      if (topAds):
        if len(topAds.findAll('div',class_='uEierd')) > 0:
          numOfTopAds += 1
        absolute_top = 0
        for container in topAds.findAll('div',class_='uEierd'):
          try:
            advertisementTitle = container.find('div',class_='CCgQ5 vCa9Yd QfkTvb MUxGbd v0nnCb').span.text
          except:
            advertisementTitle = 'N/A'

          company = container.find('div',class_='v5yQqb').find('span',class_='x2VHCd OSrXXb nMdasd qzEoUe').text
          company = tldextract.extract(company).domain

          if company not in companyList:
            companyList.append(company)
            if absolute_top == 0:
              resultDict[keyword][company] = {'absolute-top':1, 'top':0, 'bottom':0}
            else:
              resultDict[keyword][company] = {'absolute-top':0, 'top':1, 'bottom':0}
          else:
            if absolute_top == 0:
              resultDict[keyword][company]['absolute-top'] += 1
            else:
              resultDict[keyword][company]['top'] += 1

          productDescription = container.find('div',class_='MUxGbd yDYNvb lyLwlc').text

          print(advertisementTitle)
          print(company)
          print(productDescription)
          print()
          absolute_top += 1
      time.sleep(3)
      print('------------------------------------------')
      print('----------------Bottom Ads-------------------')
      bottomAds = soup.find(id='bottomads')
      if (bottomAds):
        if len(bottomAds.findAll('div',class_='uEierd')) > 0:
          numOfBottomAds += 1
        for container in bottomAds.findAll('div',class_='uEierd'):
          try:
            advertisementTitle = container.find('div',class_='CCgQ5 vCa9Yd QfkTvb MUxGbd v0nnCb').span.text
          except:
            advertisementTitle = 'N/A'

          company = container.find('div',class_='v5yQqb').find('span',class_='x2VHCd OSrXXb nMdasd qzEoUe').text
          company = tldextract.extract(company).domain

          if company not in companyList:
            companyList.append(company)
            resultDict[keyword][company] = {'absolute-top':0, 'top':0, 'bottom':1}
          else:
            resultDict[keyword][company]['bottom'] += 1

          productDescription = container.find('div',class_='MUxGbd yDYNvb lyLwlc').text

          print(advertisementTitle)
          print(company)
          print(productDescription)
          print()

      with open("output.html","w") as file:
        file.write(str(soup))

  keys = list(resultDict[keyword].keys())
  for name in ['bottom','top','absolute-top']:
    keys.sort(key=lambda k: resultDict[keyword][k][name],reverse=True)

  resultDict[keyword]['top performers'] = keys
  resultDict[keyword]['total top ads'] = numOfTopAds
  resultDict[keyword]['total bottom ads'] = numOfBottomAds

print(json.dumps(resultDict,indent=4))
