import requests
from bs4 import BeautifulSoup


main_list = []

def parsing(): 
    amount_project = 2
    count = 0


    project_name = "N/A" #v
    project_date = "N/A" #v
    funding_amount = "N/A" #v
    funding_round = "N/A" #v
    project_twitter_rating = "N/A" #v
    category = "N/A" #v
    total_investments = "N/A" #v
    twitter_link = "N/A" #v
    project_link = "N/A" #v
    result_list = []
    




    def output_console(result_list):

        project_arguments_count = 0
        output_result = ""
        
        for count in range(amount_project):

            project_arguments_count = project_arguments_count + 1

            project_name = result_list[count][0]
            project_date = result_list[count][1]
            funding_amount = result_list[count][2]
            funding_round = result_list[count][3]
            project_twitter_rating = result_list[count][4]
            category = result_list[count][5]
            investors_list = result_list[count][6]
            total_investments = result_list[count][7]
            twitter_link = result_list[count][8]
            project_link = result_list[count][9]

            result = ""
            for investor in investors_list:
                result += str(investor) + "; "
              
            output_result += f"**Название проекта:** {project_name}\n**Дата:** {project_date}\n**Сумма финансирования:** {funding_amount}\n**Тип финансирования:** {funding_round}\n**Оценка Twitter:** {project_twitter_rating}\n**Категория проекта:** {category}\n**Всего инвестиций проекта:** {total_investments}\n**Twitter:** {twitter_link} \n**Ссылка проекта:** {project_link}\n**Инвестора:**\n{result}\n\n"

        return output_result
            
            





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
                tier = investor["tier"]

                investors_list.append(f"{name}, ({tier})")
        
            return investors_list
                
        else:
            print(f"Failed to parse data. Status code: {response.status_code}")
        

    
    def func(new_list, old_list):
        global main_list
        new_projects = []
        result = ""
        for project in new_list:
            if project not in old_list:
                new_projects.append(project)
        if new_projects:
            main_list = new_list
            result = output_console(new_projects)
            return result
        else:
            print("No new projects")

    url = "https://cryptorank.io/funding-rounds"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        for cell in soup.find_all("tr", class_="sc-7ff8d1ea-0 kuuWTw init-scroll"):
            project_name = cell.find("span", class_="sc-ce25b3f-0 iTMjXc").get_text(strip=True)
            project_link = cell.find("a", class_="sc-ce25b3f-6 bQBAPp")["href"]
            full_project_link = f"https://cryptorank.io{project_link}"
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
                try:
                    total_investments = soup.find_all("p", class_="sc-50f3633f-0 fZqlZL")[1].get_text(strip=True)
                except:
                    total_investments = "N/A"

                
                
            else:
                print(f"Failed to parse data investments. Status code: {response.status_code}")


            twitter_url = url.replace("ico", "price")
            response = requests.get(twitter_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                twitter_link = soup.find_all("a", class_="sc-f910907-0 gBOfYu")[1]["href"]
                
            else:
                print(f"Failed to parse data twitter. Status code: {response.status_code}")
                

            output_list = [project_name, project_date, funding_amount, funding_round, project_twitter_rating, category, investors_list, total_investments, twitter_link, full_project_link]
            result_list.append(output_list)

            count = count + 1
            if count == amount_project: 
                break
        
        result = func(result_list, main_list)
        return result
    else:
        print(f"Failed to parse data. Status code: {response.status_code}")
        