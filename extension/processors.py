from extension.events import OpenedEventHandler, AssignedEventHandler, SubmittedEventHandler, LabeledEventHandler, \
    ReviewRequestedEventHandler, ReviewRequestRemovedEventHandler, ClosedEventHandler, EventHandler
from extension.methods import get_user_mapped_data
from extension.pull_request import PullRequest


class HookProcessor(object):
    def __init__(self, data: dict):
        self.data = data

    def process(self) -> EventHandler:
        data = self.data
        # check if the action key exists in the root level form request
        if 'action' not in data:
            raise Exception("'action' key not found in the form data")

        action = data['action']
        allowed_actions_with_parsers = {
            'opened': OpenedEventHandler,
            'assigned': AssignedEventHandler,
            'submitted': SubmittedEventHandler,
            'labeled': LabeledEventHandler,
            'review_requested': ReviewRequestedEventHandler,
            'review_request_removed': ReviewRequestRemovedEventHandler,
            'closed': ClosedEventHandler,
        }

        # check if the passed action is valid
        if action not in allowed_actions_with_parsers.keys():
            raise Exception("Invalid action requested. '{}'".format(action))

        return allowed_actions_with_parsers[action](data)


class SlackProcessor(object):
    def __init__(self, pr: PullRequest, slack_users: dict):
        self.pr = pr
        self.users = slack_users

    def process(self):
        # Prepend @ if there is any value returned, otherwise,
        if self.pr.by_git_name:
            self.pr.by = '@{}'.format(get_user_mapped_data(self.users, self.pr.by_git_name))

        if self.pr.actor_git_name:
            self.pr.actor = '@{}'.format(get_user_mapped_data(self.users, self.pr.actor_git_name))

        if self.pr.removed_reviewer_git_name:
            self.pr.removed_reviewer = '@{}'.format(get_user_mapped_data(self.users, self.pr.removed_reviewer_git_name))

        if len(self.pr.assignees_array):
            assignees = []
            for assignee in self.pr.assignees_array:
                assignees.append('@{}'.format(get_user_mapped_data(self.users, assignee)))

            self.pr.assignees = ', '.join(assignees)

        if len(self.pr.requested_reviewers_array):
            reviewers = []
            for reviewer in self.pr.requested_reviewers_array:
                reviewers.append('@{}'.format(get_user_mapped_data(self.users, reviewer)))

            self.pr.requested_reviewers = ', '.join(reviewers)

        return self.pr
