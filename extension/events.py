from abc import ABC, abstractmethod

from dotty_dict import dotty

from extension.pull_request import PullRequest


class EventHandler(ABC):
    def __init__(self, data: dict):
        self.data = dotty(data)
        self.pr = PullRequest()
        self.pr.url = self.data['pull_request.html_url']
        self.pr.repo_name = self.data['repository.full_name']
        self.pr.number = self.data['pull_request.number']
        self.pr.by = self.data['pull_request.user.login']
        self.pr.title = self.data['pull_request.title']

    @abstractmethod
    def handle(self) -> PullRequest:
        pass


class OpenedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'open'
        self.pr.assignee = self.data['pull_request.assignee.login'] if 'login' in (
                self.data['pull_request.assignee'] or []) else ''
        self.pr.reviewer = [reviewer['login'] for reviewer in self.data['pull_request.requested_reviewers']]
        self.pr.label = ', '.join([label['name'] for label in self.data['pull_request.labels']])

        return self.pr


class AssignedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'assigned'
        self.pr.assignee = self.data['pull_request.assignee.login'] if 'login' in (
                self.data['pull_request.assignee'] or []) else ''

        return self.pr


class SubmittedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'submitted'
        self.pr.by = self.data['review.user.login'] if 'login' in (self.data['review.user'] or {}) else ''
        self.pr.state = self.data['review.state']
        self.pr.comment = self.data['review.body']

        return self.pr


class LabeledEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'labeled'
        self.pr.label = ', '.join([label['name'] for label in self.data['pull_request.labels']])

        return self.pr


class ReviewRequestedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'review_requested'
        self.pr.requested_reviewers = [reviewer['login'] for reviewer in self.data['pull_request.requested_reviewers']]

        return self.pr


class ReviewRequestRemovedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'review_request_removed'
        self.pr.removed_reviewer = self.data['requested_reviewer.login'] if 'login' in (
                self.data['requested_reviewer'] or {}) else ''

        return self.pr


class ClosedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'closed'
        self.pr.state = self.data['pull_request.state']
        self.pr.is_merged = self.data['pull_request.merged']
        self.pr.merged_by = self.data['pull_request.merged_by.login'] if 'login' in (
                self.data['pull_request.merged_by'] or {}) else ''
        self.pr.merged_at = self.data['pull_request.merged_at'] or ''

        return self.pr
