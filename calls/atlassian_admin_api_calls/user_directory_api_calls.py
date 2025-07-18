import requests
from auth import atlassian_admin_Bearer_token
import json
from config import atlassian_org_api


class UserDirectory:
    def __init__(self):
        self.token = atlassian_admin_Bearer_token
        self.admin_url = atlassian_org_api
        self.org_id = 'd816j2aj-j881-10a8-7c2c-10c7736ca181'

    def restore_user(self, user_id):
        url = self.admin_url + f"{self.org_id}/directory/users/{user_id}/restore-access"

        headers = {
            "Accept": "application/json",
            "Authorization": self.token
        }

        response = requests.request(
            "POST",
            url,
            headers=headers
        )

        return response

    def suspend_user(self, user_id):
        url = self.admin_url + f"{self.org_id}/directory/users/{user_id}/suspend-access"

        headers = {
            "Accept": "application/json",
            "Authorization": self.token
        }

        response = requests.request(
            "POST",
            url,
            headers=headers
        )

        return response
