from parsing import parsing

old_list = []

async def output_console(result_list):
    result = ""
    output_list = []
    amount_count = len(result_list)
    for count in range(amount_count):
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
        
        output_result = f"**Название проекта:** {project_name}\n**Дата:** {project_date}\n**Сумма финансирования:** {funding_amount}\n**Тип финансирования:** {funding_round}\n**Оценка Twitter:** {project_twitter_rating}\n**Категория проекта:** {category}\n**Всего инвестиций проекта:** {total_investments}\n**Twitter:** {twitter_link} \n**Ссылка проекта:** {project_link}\n**Инвестора:**\n{result}\n\n"
        output_list.append(output_result)
        
    return output_list

async def control(amount_project):
    amount = amount_project
    new_list = await parsing(amount)
    global old_list
    new_projects = []
    for project in new_list:
        if project not in old_list:
            new_projects.append(project)
    if new_projects:
        old_list = new_list
        result = await output_console(new_projects)
        return result
    else:
        return None