from calls.jira_api_calls.jira_api_user_calls import UserJiraCalls
from calls.jira_api_calls.jira_api_group_calls import GroupJiraCalls
from dataformating.json_formating import JSONFormating


class Users:
    def __init__(self, is_staging=False):
        self.jira_users = UserJiraCalls(is_staging=True) if is_staging else UserJiraCalls()
        self.jira_groups = GroupJiraCalls(is_staging=True) if is_staging else GroupJiraCalls()

    def user_groups(self, user):
        groups = self.get_user_by_username(user, '?expand=groups')
        user_groups = []

        for group in groups['groups']['items']:
            user_groups.append(group['name'])

        return user_groups

    def get_user_status(self, user):
        user_profile = self.get_user_by_username(user)
        if user_profile['active']:
            return 'Active'
        else:
            return 'Inactive'

    def get_user_applications(self, user):
        user_profile = self.get_user_by_username(user, '?expand=applicationRoles')
        roles = []
        for role in user_profile['applicationRoles']['items']:
            roles.append(role['name'])

        return roles

    def delete_list_of_users(self, users):
        for user in users:
            response = self.jira_users.delete_user(user)
            print(response)

    def get_usernames_by_domain_string(self, users_search_string):
        start_at = 0
        max_results = 50
        total = 51
        users_found = []
        while total >= max_results:
            users = self.jira_groups.get_group(f'?includeInactiveUsers=false&startAt={start_at}'
                                              f'&maxResults={max_results}&includeInactive=True', 'app-jira')
            for user in users['values']:
                if users_search_string in user['emailAddress']:
                    users_found.append(user['name'])

            print(users_found)
            print(total, start_at, max_results)
            total = users['total']
            start_at += 50
            max_results += 50

        return users_found

    def get_user_by_username(self, username, pref=''):
        query = {
            'username': username,
        }
        user = self.jira_users.get_user(query, pref)
        return user

    def get_user_by_id(self, user_id, pref=''):
        query = {
            'accountId': user_id
        }
        user = self.jira_users.get_user(query, pref)
        return user
