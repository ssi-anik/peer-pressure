from abc import ABC, abstractmethod

from extension.pull_request import PullRequest


class Medium(ABC):
    def __init__(self, users, pr: PullRequest):
        self.users = users
        self.pr = pr

    @abstractmethod
    def notify(self):
        pass


class Slack(Medium):
    def notify(self):
        print(self.pr.assignee)
        pass


class Email(Medium):
    def notify(self):
        pass
