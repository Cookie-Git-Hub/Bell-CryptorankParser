import requests
from bs4 import BeautifulSoup

project_name = "N/A" #v
project_date = "N/A" #v
funding_amount = "N/A" #v
funding_round = "N/A" #v
project_twitter_rating = "N/A" #v
category = "N/A" #v
project_total_investments = "N/A" #v
twitter_link = "N/A" #v



def output_console(project_name, project_date, funding_amount, funding_round, project_twitter_rating, category, investors_list, project_total_investments, twitter_link):
    print("**Название проекта:**", project_name)
    print("**Дата:**", project_date)
    print("**Сумма финансирования:**", funding_amount)
    print("**Тип финансирования:**", funding_round)
    print("**Оценка Twitter:**", project_twitter_rating)
    print("**Категория проекта:**", category)

    print("**Всего инвестиций проекта:**", project_total_investments)
    print("**Twitter:**", twitter_link)

    print("**Инвестора:**")
    for investor in investors_list:
        print(investor)
        
    print("------------------------------------")



def parsing_investors(project_name):
    name = project_name.lower().replace(".", "-").replace(" ", "-")
    
    url = f"https://api.cryptorank.io/v0/coins/{name}/investors-list?limit=10&skip=0"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  
        investors = data['investors']
        
        investors_list = []
        for investor in investors:
            name = investor["name"]
            tier = investor['tier']
            category = investor['category']
            stage = investor['stage']
            investors_list.append(f"Инвестор: {name}, Стадия: {tier}, Категория: {category}, Stage: {stage}")
    
        return investors_list
             
    else:
        print(f"Failed to parse data. Status code: {response.status_code}")
    



url = "https://cryptorank.io/funding-rounds"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    count = 0

    for cell in soup.find_all("tr", class_="sc-7ff8d1ea-0 kuuWTw init-scroll"):

        count = count + 1

        project_name = cell.find("span", class_="sc-ce25b3f-0 iTMjXc").get_text(strip=True)
        project_link = cell.find("a", class_="sc-ce25b3f-6 bQBAPp")["href"]
        project_date = cell.find("td", class_="sc-c79f6d7-0 jehnNa sc-688d708a-0 gWxWSW").get_text(strip=True)
        funding_amount = cell.find("td", class_="sc-c79f6d7-0 ftkmA-D sc-ebc32dcf-0 ja-DHql").get_text(strip=True)
        funding_round = cell.find("td", class_="sc-c79f6d7-0 jehnNa").get_text(strip=True)
        twitter_rating = cell.find("span", class_="sc-50f3633f-0 iXtZYt")
        if twitter_rating:
            project_twitter_rating = twitter_rating.text
        category = cell.find("p", class_="sc-50f3633f-0 crWDxH").get_text(strip=True)

        
        investors_list = parsing_investors(project_name)  
            
         
        url = f"https://cryptorank.io{project_link}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            total_investments = soup.find_all("p", class_="sc-50f3633f-0 fZqlZL")[1].get_text(strip=True)
            
            
        else:
            print(f"Failed to parse data investments. Status code: {response.status_code}")


        twitter_url = url.replace("ico", "price")
        response = requests.get(twitter_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            twitter_link = soup.find_all("a", class_="sc-f910907-0 gBOfYu")[1]["href"]
            
        else:
            print(f"Failed to parse data twitter. Status code: {response.status_code}")
            

        output_console(project_name, project_date, funding_amount, funding_round, project_twitter_rating, category, investors_list, total_investments, twitter_link)

        if count == 2: 
            break
else:
    print(f"Failed to parse data. Status code: {response.status_code}")
    
    
    
    

