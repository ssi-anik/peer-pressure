from abc import ABC, abstractmethod

import requests

from extension.pull_request import PullRequest


class Medium(ABC):
    def __init__(self, pr: PullRequest, messages: dict):
        self.pr = pr
        self.messages = messages

    @abstractmethod
    def notify(self):
        pass


class Slack(Medium):

    def __init__(self, pr: PullRequest, messages: dict, conf: dict):
        super().__init__(pr, messages)
        self.conf = conf

    def notify(self):

        if self.pr.action == 'opened':
            message = self.messages['opened'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'assigned':
            message = self.messages['assigned'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'labeled':
            message = self.messages['labeled'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'review_requested':
            message = self.messages['review_requested'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'review_request_removed':
            message = self.messages['review_request_removed'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'merged':
            message = self.messages['merged'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'closed':
            message = self.messages['closed'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'approved':
            message = self.messages['approved'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'commented':
            message = self.messages['commented'].format(**self.pr.get_as_dict())
        elif self.pr.action == 'changes_requested':
            message = self.messages['changes_requested'].format(**self.pr.get_as_dict())
        else:
            message = self.messages['default'] \
                if 'default' in self.messages \
                else '@channel, something happened :gun: on {url}'.format(**self.pr.get_as_dict())

        data = {
            'channel': '#{}'.format(self.conf.get('channel').lstrip('#')),
            'link_names': 1,
            'text': message,
        }

        if self.conf.get('username'):
            data['username'] = self.conf.get('username')

        if self.conf.get('emoji'):
            data['icon_emoji'] = self.conf.get('emoji')

        url = self.conf.get('url').strip()
        if not url:
            raise Exception('Slack URL is not given')

        try:
            print(data)
            r = requests.post(url, json=data, headers={'Content-type': 'application/json'})
            print('Response: {}'.format(r.content))
        except Exception as e:
            print(str(e))
