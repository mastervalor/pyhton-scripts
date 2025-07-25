import unittest
from calls.atlassian_admin_api_calls.auth_policies_api import AtlassianAuthPolicies


class TestAuthPolicies(unittest.TestCase):
    def setUp(self):
        self.auth_policies = AtlassianAuthPolicies()

    def test_add_users_to_policy(self):
        users = ['test-user@getcruise.com']
        new_policy = "3b93d6bc-1087-427f-b1a9-0dacc7bb837f"
        response = self.auth_policies.add_users_to_policy(users, new_policy)
        self.assertIn('taskId', response)

    def test_get_task_status(self):
        task_id = 'f39e9fc7-1a83-47d0-9a82-f8e76f878558'
        response = self.auth_policies.get_task_status(task_id).json()
        self.assertIn('inProgressCount', response)

    def test_invalid_get_task_status(self):
        task_id = 'apple'
        response = self.auth_policies.get_task_status(task_id)
        self.assertEqual(response.status_code, 400)
