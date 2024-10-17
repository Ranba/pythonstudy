import requests
from bs4 import BeautifulSoup

# 爬取GitHub项目内容的函数
def scrape_github_project(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 发起请求
    response = requests.get(url, headers=headers)
    
    # 如果请求成功，解析页面内容
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取项目名称
        project_name = soup.find('strong', {'itemprop': 'name'}).text.strip()
        
        # 获取项目 star 数量
        stars_element = soup.find('span', {'id': 'repo-stars-counter-star'})
        stars = stars_element.text.strip() if stars_element else "N/A"
        
        # 获取项目描述 (About)
        about_section = soup.find('p', {'class': 'f4 my-3'})
        about = about_section.text.strip() if about_section else "No description provided."

        # 获取README内容
        readme_section = soup.find('article', {'class': 'markdown-body entry-content'})
        readme_content = readme_section.text.strip() if readme_section else "README not found."

        # 返回爬取的信息
        return {
            "name": project_name,
            "url": url,
            "stars": stars,
            "about": about,
            "readme": readme_content
        }
    else:
        return None

# 将爬取的结果保存为 Markdown 文件
def save_to_markdown(project_data):
    project_name_clean = project_data['name'].replace(" ", "_")  # 将空格替换为下划线，防止文件名问题
    output_md = f'{project_name_clean}.md'
    output_readme = f'{project_name_clean}_README.md'
    
    # 保存项目的元数据 Markdown 文件
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(f"# {project_data['name']}\n\n")
        f.write(f"**Project URL**: [{project_data['url']}]({project_data['url']})\n\n")
        f.write(f"**Stars**: {project_data['stars']}\n\n")
        f.write(f"**About**: {project_data['about']}\n")
    
    # 保存 README 文件
    with open(output_readme, 'w', encoding='utf-8') as f:
        f.write(project_data['readme'])
    
    return output_md, output_readme

# 示例：爬取某个GitHub项目的信息
if __name__ == '__main__':
    # 让用户输入GitHub项目的URL
    github_project_url = input("Please enter the GitHub project URL: ").strip()

    # 爬取项目内容
    project_info = scrape_github_project(github_project_url)
    
    if project_info:
        # 保存到以项目名称命名的 Markdown 和 README 文件
        markdown_file_path, readme_file_path = save_to_markdown(project_info)
        print(f"Project information saved to {markdown_file_path}")
        print(f"README saved to {readme_file_path}")
