import pytest
from src.user import User

@pytest.fixture
def valid_user():
    return User("Alice", "alice@example.com", 25)

@pytest.fixture
def premium_user():
    return User("Kate", "kate@example.com", 30, status="Premium")

class TestUser:
    # successful user creation
    def test_user_creation_valid_data(self, valid_user):
        assert valid_user.name == "Alice"
        assert valid_user.email == "alice@example.com"
        assert valid_user.age == 25
        assert valid_user.status == "Standard"

    # age validation (minimum 13 years old)
    def test_user_too_young(self):
        user = User("Mark", "mark@example.com", 10)
        assert user.age == "Invalid"

    # basic email format validation
    def test_user_invalid_email(self):
        user = User("John", "john-at-work.example.com", 30)
        assert user.email == "Invalid"

    # premium functionality - saving goals limit
    def test_standard_user_goals_limit(self, valid_user):
        first_goal = valid_user.add_saving_goal("New Car")
        assert first_goal is True
        
        # standard user should not be able to add a second goal
        second_goal = valid_user.add_saving_goal("Vacation")
        assert second_goal is False
        assert len(valid_user.saving_goals) == 1

    def test_premium_user_multiple_goals(self, premium_user):
        premium_user.add_saving_goal("New Car")
        premium_user.add_saving_goal("Vacation")
        premium_user.add_saving_goal("House")
        assert len(premium_user.saving_goals) == 3

    # status upgrade
    def test_upgrade_to_premium(self, valid_user):
        valid_user.upgrade_to_premium()
        assert valid_user.status == "Premium"