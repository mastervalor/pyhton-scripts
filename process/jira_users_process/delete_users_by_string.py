from logic.jira_logic.user_logic import Users
from file_manip.csv_file_manip import CSVLogic

user = Users(is_staging=True)
csv_logic = CSVLogic(open_file='username')
file = csv_logic.read_file()
users = []

for username in file:
    users.append(username['Full name'])

user.delete_list_of_users(users)
