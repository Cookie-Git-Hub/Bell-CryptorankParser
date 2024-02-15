import requests
from bs4 import BeautifulSoup


def output_console(project_name, project_link, project_date, funding_amount, funding_round, project_text_content, project_twitter_rating, category, project_total_investments, project_name_investor, project_tier, project_type, project_stage, project_twitter, count):
    print("Название проекта:", project_name)
    print("Ссылка проекта:", project_link)
    print("Дата:", project_date)
    print("Сумма финансирования:", funding_amount)
    print("Тип финансирования:", funding_round)
    print("Название фонда:", project_text_content)
    print("Оценка Twitter:", project_twitter_rating)
    print("Категория проекта", category)
    print("Всего инвестиций:", project_total_investments)
    print("Название инвестора", project_name_investor)
    print("Уровень проекта:", project_tier)
    print("Тип проекта", project_type)
    print("Стадия проекта", project_stage)
    print("Twitter", project_twitter)
    print("Count", count)
    print("------------------------------------")


def additional_information(project_link, project_name):
    url1 = f"https://cryptorank.io{project_link}"
    response1 = requests.get(url1)

    if response1.status_code == 200:
        soup = BeautifulSoup(response1.content, "html.parser")
        
        total_investments = soup.find_all("p", class_="sc-50f3633f-0 fZqlZL")
        t_inv = total_investments[1]
        if t_inv:
            investments = t_inv.text

        for cell in soup.find_all("tr", class_="sc-7ff8d1ea-0 kuuWTw init-scroll"):

        
            name = cell.find("p", class_="sc-c79f6d7-0 hMPVxR").get_text(strip=True)
            tier = cell.find("p", class_="sc-c79f6d7-0 dmCzJN").get_text(strip=True)
            type = cell.find("p", class_="sc-c79f6d7-0 bCesSr").get_text(strip=True)
            stage = cell.find("p", class_="sc-c79f6d7-0 fBhYIE").get_text(strip=True)

            url2 = f"https://cryptorank.io/price/{project_name.lower()}"
            response2 = requests.get(url2)

            if response2.status_code == 200:
                a = BeautifulSoup(response2.content, "html.parser")

                twitter = a.find("div", class_="sc-be4b7d84-0 dtQbLH").get_text(strip=True)

            else:
                print("Ошибка при получении данных в additional_information url2. Код статуса:", response2.status_code)
                return None
                
            
            print("Название инвестора", name)
            print("Уровень проекта:", tier)
            print("Тип проекта", type)
            print("Стадия проекта", stage)
            print("Twitter", twitter)

            return {
                'project_total_investments': investments, 
                'project_name_investor': name, 
                'project_tier': tier, 
                'project_type': type, 
                'project_stage': stage, 
                'project_twitter': twitter
            }
        

    else:
        print("Ошибка при получении данных в additional_information url1. Код статуса:", response1.status_code)
        return None



saved_data = []

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
        fund_name = cell.find("span", class_="sc-a3b70ab2-3 liNnOB")
        if fund_name:
            project_text_content = fund_name.text
        twitter_rating = cell.find("span", class_="sc-50f3633f-0 iXtZYt")
        if twitter_rating:
            project_twitter_rating = twitter_rating.text
        category = cell.find("p", class_="sc-50f3633f-0 crWDxH").get_text(strip=True)

        add = additional_information(project_link, project_name)

        project_total_investments = ""
        project_name_investor = ""
        project_tier = ""
        project_type = ""
        project_stage = ""
        project_twitter = ""

        if add is not None:
            project_total_investments = add.get('project_total_investments')
            project_name_investor = add.get('project_name_investor')
            project_tier = add.get('project_tier')
            project_type = add.get('project_type')
            project_stage = add.get('project_stage')
            project_twitter = add.get('project_twitter')
        else:
            print("Ошибка")

        output_console(project_name, project_link, project_date, funding_amount, funding_round, project_text_content, project_twitter_rating, category, project_total_investments, project_name_investor, project_tier, project_type, project_stage, project_twitter, count)

        if count == 3:
            break
else:
    print("Ошибка при получении данных. Код статуса:", response.status_code)


# def array_compare(arr):
#     for i
