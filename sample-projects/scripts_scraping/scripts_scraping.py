import requests
from bs4 import BeautifulSoup

root="https://subslikescript.com/"
result=requests.get("https://subslikescript.com/movies")




content=result.text
soup=BeautifulSoup(content,'lxml')
# print(soup.prettify())
# soup.find_all("h2")
pagination=soup.find('ul',class_='pagination')
pages=pagination.find_all('li',class_='page-item')
last_page=pages[-2].text
print(last_page)

for page in range(1,5):
    page=f'{root}/movies?page={page}'
    new_page=requests.get(page)
    new_page_content=new_page.text
    page_soup=BeautifulSoup(content,'lxml')
    box=soup.find('article',class_='main-article')
    links=[]
    for link in box.find_all('a',href=True):
        links.append(link['href'])
        
    failed_links=[]
    for link in links:
        try:
            print("Sraping link", link)
            page_link=f'{root}/{link}'
            new_script=requests.get(page_link)
            content=new_script.text
            soup=BeautifulSoup(content,'lxml')
            title=box.find('h1').get_text()
            box=soup.find('article',class_='main-article')
            transcript=box.find('div',class_='full-script').get_text(strip=True,separator=' ')
            print(title)
            # print(transcript)
        
            with open(f'scripts/{title}.txt','w') as file:
                file.write(transcript)
                print("Scraping completed successfully")
        except:
            print("Scraping failed\n",link)
            failed_links.append(link)
    print(failed_links)