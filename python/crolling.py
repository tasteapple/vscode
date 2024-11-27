import requests
from bs4 import BeautifulSoup

url = 'https://www.yna.co.kr/sports/all'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    news_titles = soup.find_all('strong', class_='tit-news')
    news_links = soup.find_all('a', class_='tit-wrap')

    with open('news_scrap.txt', 'w', encoding='utf-8') as file:
        cnt = 0
        for link in news_links:
            file.write('기사 제목: ')
            file.write(news_titles[cnt].text)
            file.write('\n')
            cnt += 1
            url2 = str(link.get('href'))

            response2 = requests.get(url2)
            
            if response2.status_code == 200:
                html2 = response2.text
                soup2 = BeautifulSoup(html2, 'html.parser')

                article = soup2.find('article', class_='story-news article')
                if not article:
                    file.write('본문 없음\n')
                    continue

                comp_box_zone = article.find('div', class_='comp-box photo-group')
                if comp_box_zone:
                    comp_box_zone.decompose()

                txt_copyright_zone = article.find('p', class_='txt-copyright adrs')
                if txt_copyright_zone:
                    txt_copyright_zone.decompose()

                sentences = article.find_all('p')
                for sentence in sentences:
                    file.write(sentence.text)
                    file.write('\n')
                file.write('\n')

else:
    print('URL 요청 실패')
