from django.contrib.auth.models import User
from django.test import TestCase


TEST_FIRST_NAME = 'test_first_name'
TEST_LAST_NAME = 'test_last_name'
TEST_EMAIL = 'test123@test.com'
TEST_USERNAME = 'test123'
TEST_PASSWORD = 'test123'
TEST_BIRTH_DATE = '1990-01-01'
TEST_GENDER = 'm'
TEST_LOCATION = 'somewhere'
 
class LoginTestCase(TestCase):
    def setUp(self):
        # create test test_user
        self.test_user = User.objects.create_user(
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
        )
        self.test_user.profile.birth_date = TEST_BIRTH_DATE
        self.test_user.profile.location = TEST_LOCATION
        self.test_user.profile.gender = TEST_GENDER
        self.test_user.is_active = True
        self.test_user.save()

    def tearDown(self):
        User.objects.get(username=TEST_USERNAME).delete()
    
    def test_user_first_name_set_correctly(self):
        self.assertEqual(self.test_user.first_name, TEST_FIRST_NAME)
        
    def test_user_first_name_set_correctly(self):
        self.assertEqual(self.test_user.last_name, TEST_LAST_NAME)
        
    def test_user_email_set_correctly(self):
        self.assertEqual(self.test_user.email, TEST_EMAIL)
        
    def test_user_birth_date_set_correctly(self):
        self.assertEqual(self.test_user.profile.birth_date, TEST_BIRTH_DATE)
        
    def test_user_gender_set_correctly(self):
        self.assertEqual(self.test_user.profile.gender, TEST_GENDER)
        
    def test_user_location_set_correctly(self):
        self.assertEqual(self.test_user.profile.location, TEST_LOCATION)        
        