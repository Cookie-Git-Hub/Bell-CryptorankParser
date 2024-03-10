import aiohttp
from bs4 import BeautifulSoup

async def parsing_investors(session, project_link):
    link = project_link.lower().replace("/ico/", "")
    url = f"https://api.cryptorank.io/v0/coins/{link}/investors-list?limit=10&skip=0"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                investors = data['investors']
                investors_list = [f"{investor['name']}, ({investor['tier']})" for investor in investors]
                return investors_list
            else:
                print(f"Failed to parse data. Status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Failed to fetch data from Cryptorank API: {e}")
        return None

async def parsing(amount_project):
    count = 0
    result_list = []
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cryptorank.io/funding-rounds") as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                for cell in soup.find_all("tr", class_="sc-7ff8d1ea-0 kuuWTw init-scroll"):
                    project_name = cell.find("span", class_="sc-ce25b3f-0 iTMjXc").get_text(strip=True)
                    project_link = cell.find("a", class_="sc-ce25b3f-6 bQBAPp")["href"].replace("#funding-rounds", "")
                    full_project_link = f"https://cryptorank.io{project_link}"
                    project_date = cell.find("td", class_="sc-67ec7576-0 dEZesu sc-688d708a-0 gWxWSW").get_text(strip=True)
                    funding_amount = cell.find("td", class_="sc-67ec7576-0 cqMRXb sc-ebc32dcf-0 ja-DHql").get_text(strip=True)
                    funding_round = cell.find("td", class_="sc-67ec7576-0 dEZesu").get_text(strip=True)
                    twitter_rating = cell.find("span", class_="sc-67ec7576-0 bwSdbV")
                    project_twitter_rating = twitter_rating.text if twitter_rating else "N/A"
                    category = cell.find("p", class_="sc-50f3633f-0 crWDxH").get_text(strip=True)

                    investors_list = await parsing_investors(session, project_link)

                    url = f"https://cryptorank.io{project_link}"
                    async with session.get(url) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, "html.parser")
                            try:
                                total_investments = soup.find_all("p", class_="sc-50f3633f-0 fZqlZL")[1].get_text(strip=True)
                            except:
                                total_investments = "N/A"
                        else:
                            print(f"Failed to parse data investments. Status code: {response.status}")

                    twitter_url = url.replace("ico", "price")
                    async with session.get(twitter_url) as response:
                        if response.status == 200:
                            twitter_link = ""
                            html = await response.text()
                            soup = BeautifulSoup(html, "html.parser")
                            links = soup.find_all("a", class_="sc-f910907-0 gBOfYu")
                            for link in links:
                                if link["href"].startswith("https://twitter.com"):
                                    twitter_link = link["href"]
                                    break
                                else:
                                    twitter_link = "N/A"
                        else:
                            print(f"Failed to parse data twitter. Status code: {response.status}")
                    output_list = [project_name, project_date, funding_amount, funding_round, project_twitter_rating, category, investors_list, total_investments, twitter_link, full_project_link]
                    result_list.append(output_list)

                    count += 1
                    if count == amount_project:
                        break
                return result_list
            else:
                print(f"Failed to fetch data from https://cryptorank.io/funding-rounds. Status code: {response.status}")

