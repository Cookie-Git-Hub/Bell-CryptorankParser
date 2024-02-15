import requests
from bs4 import BeautifulSoup

url = "https://cryptorank.io/funding-rounds"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    projects = soup.find_all("tbody", class_="sc-441b296f-1 goTVrV")
    
    for project in projects:
        project_name = project.find("span", class_="sc-cmTdod sc-dlfnbm sc-hlILoM bpcwRJ").text.strip()
        project_link = project.find("a", class_="sc-cmTdod sc-dlfnbm sc-jQCOkK fiKhuw")["href"]
        date = project.find("td", class_="sc-dVhcbM sc-kiVfSS keRtBr").text.strip()
        funding_amount = project.find("td", class_="sc-dVhcbM sc-cQFLBn gZOXgL").text.strip()
        funding_round = project.find("td", class_="sc-dVhcbM sc-kiVfSS keRtBr").find_next_sibling().text.strip()
        fund_name = project.find("span", class_="sc-cmTdod sc-dlfnbm sc-hlILoM bpcwRJ").find_next_sibling().text.strip()
        twitter_rating = project.find("div", class_="sc-iwsKbI ceYwLP").text.strip()
        
        print("Название проекта:", project_name)
        print("Ссылка проекта:", project_link)
        print("Дата:", date)
        print("Сумма финансирования:", funding_amount)
        print("Тип финансирования:", funding_round)
        print("Название фонда:", fund_name)
        print("Оценка Twitter:", twitter_rating)
        print("------------------------------------")
else:
    print("Ошибка при получении данных. Код статуса:", response.status_code)
