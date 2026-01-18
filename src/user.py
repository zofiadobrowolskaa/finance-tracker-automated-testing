import re

class User:
    def __init__(self, name, email, age, status="Standard"):
        self.name = name
        self.age = age if self._is_age_valid(age) else "Invalid"
        self.email = email if self._is_email_valid(email) else "Invalid"
        self.status = status
        self.saving_goals = []

    def _is_age_valid(self, age):
        return isinstance(age, int) and age >= 13

    def _is_email_valid(self, email):
        if not isinstance(email, str):
            return False

        email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return bool(re.match(email_regex, email))

    def add_saving_goal(self, goal_name):
        if self.status == "Standard" and len(self.saving_goals) >= 1:
            return False
        
        self.saving_goals.append(goal_name)
        return True

    def upgrade_to_premium(self):
        self.status = "Premium"