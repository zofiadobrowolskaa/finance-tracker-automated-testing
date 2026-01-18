import re

class User:
    def __init__(self, name, email, age, status="Standard"):
        self.name = name
        self.age = age if age >= 13 else "Invalid"
        self.email = email if self._validate_email(email) else "Invalid"
        self.status = status
        self.saving_goals = []

    def _validate_email(self, email):
        email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if re.match(email_regex, email):
            return True
        return False

    def add_saving_goal(self, goal_name):
        if self.status == "Standard" and len(self.saving_goals) >= 1:
            return False
        
        self.saving_goals.append(goal_name)
        return True

    def upgrade_to_premium(self):
        self.status = "Premium"