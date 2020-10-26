from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sql_user_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests the multiple routes of Users"""

    def setUp(self):
        """ Add a sample User """
        User.query.delete()

        user = User(
            first_name="TestSurname",
            last_name="TestFamilyName",
            image_url="https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png",
        )
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any stale transactions"""
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_detail_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestSurname", html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("</label>", html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("</label>", html)
