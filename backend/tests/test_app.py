import unittest
from unittest.mock import patch
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'username': 'testuser',
                'email': 'test@example.com',
                'name': 'Test User'
            }

    def test_get_courses_list(self):
        response = self.client.get('/api/courses_list')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_test_courses(self):
        response = self.client.get('/api/test_courses')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)

    def test_get_user(self):
        response = self.client.get('/get-user')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['username'], 'Test User')

    @patch('app.db')
    def test_get_user_courses(self, mock_db):
        mock_db["user-courses"].find_one.return_value = {
            "username": "testuser", "courses": ["ECS120", "ECS150"]
        }
        response = self.client.get('/api/user/courses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), ["ECS120", "ECS150"])

    @patch('app.db')
    def test_add_user_course(self, mock_db):
        mock_db["user-courses"].find_one.return_value = {
            "username": "testuser", "courses": []
        }
        mock_db["user-courses"].update_one.return_value.matched_count = 1
        response = self.client.put('/api/user/courses/add', json={"course": "ECS120"})
        self.assertEqual(response.status_code, 201)

    @patch('app.db')
    def test_remove_user_course(self, mock_db):
        mock_db["user-courses"].find_one.return_value = {
            "username": "testuser", "courses": ["ECS120"]
        }
        mock_db["user-courses"].update_one.return_value.matched_count = 1
        response = self.client.put('/api/user/courses/remove', json={"course": "ECS120"})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()