from abc import ABC, abstractmethod

from dotty_dict import dotty

from extension.pull_request import PullRequest


class EventHandler(ABC):
    def __init__(self, data: dict):
        self.data = dotty(data)
        self.pr = PullRequest()
        self.pr.url = self.data['pull_request.html_url']
        self.pr.repo = self.data['repository.full_name']
        self.pr.repo_url = self.data['repository.html_url']
        self.pr.number = self.data['pull_request.number']
        self.pr.by_git_name = self.data['pull_request.user.login']
        self.pr.title = self.data['pull_request.title']
        self.pr.head = self.data['pull_request.head.label']
        self.pr.base = self.data['pull_request.base.label']
        self.pr.actor_git_name = self.data['sender.login'] or 'N/A'

    @abstractmethod
    def handle(self) -> PullRequest:
        pass


class OpenedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'opened'
        self.pr.assignees_array = [
            assignee['login'] for assignee in (self.data['pull_request.assignees'] or [])
        ]
        self.pr.requested_reviewers_array = [
            reviewer['login'] for reviewer in (self.data['pull_request.requested_reviewers'] or [])
        ]
        self.pr.labels = ', '.join([label['name'] for label in (self.data['pull_request.labels'] or [])])

        return self.pr


class AssignedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'assigned'
        self.pr.assignees_array = [
            assignee['login'] for assignee in (self.data['pull_request.assignees'] or [])
        ]

        return self.pr


class SubmittedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'submitted'
        self.pr.state = self.data['review.state'] or 'commented'
        self.pr.comment = self.data['review.body'] or ''
        self.pr.assignees_array = [
            assignee['login'] for assignee in (self.data['pull_request.assignees'] or [])
        ]

        if self.pr.state == 'approved':
            self.pr.action = 'approved'
        elif self.pr.state == 'commented':
            self.pr.action = 'commented'
        elif self.pr.state == 'changes_requested':
            self.pr.action = 'changes_requested'

        return self.pr


class LabeledEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'labeled'
        self.pr.labels = ', '.join([label['name'] for label in (self.data['pull_request.labels'] or [])])

        return self.pr


class ReviewRequestedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'review_requested'
        self.pr.requested_reviewers_array = [
            reviewer['login'] for reviewer in (self.data['pull_request.requested_reviewers'] or [])
        ]

        return self.pr


class ReviewRequestRemovedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'review_request_removed'
        self.pr.removed_reviewer_git_name = self.data['requested_reviewer.login'] if 'login' in (
                self.data['requested_reviewer'] or {}
        ) else ''
        self.pr.requested_reviewers_array = [
            reviewer['login'] for reviewer in (self.data['pull_request.requested_reviewers'] or [])
        ]

        return self.pr


class ClosedEventHandler(EventHandler):
    def handle(self) -> PullRequest:
        self.pr.action = 'closed'
        self.pr.state = self.data['pull_request.state']
        self.pr.is_merged = self.data['pull_request.merged']
        self.pr.merged_by = self.data['pull_request.merged_by.login'] if 'login' in (
                self.data['pull_request.merged_by'] or {}
        ) else 'N/A'
        self.pr.merged_at = self.data['pull_request.merged_at'] or ''

        if self.pr.is_merged:
            self.pr.action = 'merged'

        return self.pr
