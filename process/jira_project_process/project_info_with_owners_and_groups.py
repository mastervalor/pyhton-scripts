from logic.jira_logic.project_logic import Projects
from file_manip.csv_file_manip import CSVLogic

project_logic = Projects()
csv_logic = CSVLogic(open_file='Archived projects - projects to standerdize', write_file='all projects')
file = csv_logic.read_file()
archived_projects = []
projects_table = []

for project in file:
    archived_projects.append(project['project_key'])


def project_info():
    projects_table = []
    projects = project_logic.get_project_owners_and_status()

    for project in projects:
        if project['Key'] not in archived_projects:
            projects_table.append(project_logic.build_project_table(project['Project'], project['Key'], project['Name'],
                                                                    project['Active']))

    return projects_table
