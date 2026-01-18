import pytest
from src.user import User

class TestUser:
    # successful user creation
    def test_user_creation_valid_data(self):
        user = User("Alice", "alice@example.com", 25)
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.age == 25
        assert user.status == "Standard"

    # age validation (minimum 13 years old)
    def test_user_too_young(self):
        user = User("Mark", "mark@example.com", 10)
        assert user.age == "Invalid"

    # basic email format validation
    def test_user_invalid_email(self):
        user = User("John", "john-at-work.example.com", 30)
        assert user.email == "Invalid"

    # premium functionality - saving goals limit
    def test_standard_user_goals_limit(self):
        user = User("John", "john@example.com", 30)
        first_goal = user.add_saving_goal("New Car")
        assert first_goal is True
        
        # standard user should not be able to add a second goal
        second_goal = user.add_saving_goal("Vacation")
        assert second_goal is False
        assert len(user.saving_goals) == 1

    def test_premium_user_multiple_goals(self):
        user = User("Kate", "kate@example.com", 30, status="Premium")
        user.add_saving_goal("New Car")
        user.add_saving_goal("Vacation")
        user.add_saving_goal("House")
        assert len(user.saving_goals) == 3

    # Status upgrade
    def test_upgrade_to_premium(self):
        user = User("Rose", "rose@example.com", 22)
        user.upgrade_to_premium()
        assert user.status == "Premium"