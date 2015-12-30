import requests
from bs4 import BeautifulSoup
from crawl.models import News

hacker_urls = ['https://news.ycombinator.com/newest','https://news.ycombinator.com/newest?next=10805439&n=31','https://news.ycombinator.com/newest?next=10805116&n=61']
result = []
output_text = []

for hurl in hacker_urls:
    response = requests.get(hurl)
    html = response.content

    soup = BeautifulSoup(html)
    table = soup.find('table', attrs={'class': 'itemlist'})

    data = 0
    temp_list = []
    href_active = 0

    for row in table.findAll('tr'):
    
        for cell in row.findAll('td'):
            text = cell.text
            if len(text) > 10:
           
                if data == 0:
                    for url in cell.findAll('a'):
                        href = url['href']
                        if href_active == 0:
                            temp_list.append(str(href))
                            href_active = 1
                        else:
                            href_active = 0
                        n_text = url.text
                        temp_list.append(n_text)
                    data = 1
                else:
                    data = 0
                    for val in cell.findAll('span'):
                        n_text = val.text
                        temp_list.append(n_text)
                        
                    for url in cell.findAll('a'):
                        href = url['href']
                        n_text = url.text
                        temp_list.append(n_text)
                    #temp_list.append(str(hurl))
                    output_text.append(temp_list)
                    temp_list = []


index = 0
temp_list = []
for val in output_text:
    len_val = len(val) - 1
    for data in val:
        if index == 0:
            temp_list.append(data)
            index = index + 1
        elif index == 1:
            temp_list.append(data)
            index = index + 1
        elif index == 2:
            temp_list.append(data)
            index = index + 1
        elif index == len_val:
            temp_list.append(data)
            index = index + 1
        elif 'point' in data:
            if len(data) < 10:
                temp_list.append(data)
            index = index + 1
        elif 'comment' in data:
            if len(data) < 10:
                temp_list.append(data)
            index = index + 1
        else:
            index = index + 1
    result.append(temp_list)
    index = 0
    temp_list = []

def populate_data(data,length):
    news_url = data[0]
    title = data[1]
    source = data[2]
    upvote = '0 point'
    comment = '0 comment'
    
    if 'http' in data[0]:
        news_url = data[0]
        title = data[1]
        source = data[2]
        upvote = '0 point'
        comment = '0 comment'
        if 'point' in data[3]:
            upvote = data[3]
        elif 'comment' in data[3]:
            comment = data[3]
        
        if 'comment' in data[4]:
            comment = data[4] 
    
        already_there = News.objects.filter(news_url__iexact=news_url,source__iexact=source,title__iexact=title)
        if bool(already_there):
            for news in already_there:
                print(news.title)
                news.upvote = upvote
                news.comment = comment
                news.save()
        else:
            obj = News.objects.create(news_url=news_url,title=title,source=source,upvote=upvote,comment=comment)

for data in result:
    populate_data(data,len(data))