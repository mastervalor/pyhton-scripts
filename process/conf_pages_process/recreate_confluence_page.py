from logic.confluence_logic.page_logic import Pages
from process.jira_project_process.project_info_with_owners_and_groups import project_info
import html

page = Pages()

projects = project_info()
parent_page = '421062700'
target_page = '355776435'
title = 'table create test from script four'
space_key = 'IT'
projects_dict = []

clear_page = page.clear_page_content(target_page)

for row in projects:
    approver = row['Approver']
    if '[C]' in approver:
        approver = approver.replace('[C]', '')
    if '[GM]' in approver:
        approver = approver.replace('[GM]', '')

    row['Name'] = html.escape(row['Name'])
    row['key'] = html.escape(row['Key'])
    row['username'] = html.escape(approver)
    projects_dict.append({
        "project_name": row['Name'],
        "project_key": row['key'],
        "approver": row['username'],
        "admin_group": row['Admin group'],
        "developer_group": row['Developer group'],
        "user_group": row['User group'],
        "agent_group": row['Agent group'],
        "project_type": row['Project type']
    })

# Define the table headers
table_headers = ["Project Name", "Project Key", "Approver", "Admin Group", "Developer Group", "User Group",
                 "Agent Group", "Project Type"]

table_content = page.generate_table_content(projects_dict, table_headers)

page_version = page.get_page_version(target_page)

# Create the Confluence page
response = page.update_page(target_page, title, table_content)

if response:
    print('Page created successfully:', response)
else:
    print('Failed to create the page.')