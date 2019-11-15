from extension.events import OpenedEventHandler, AssignedEventHandler, SubmittedEventHandler, LabeledEventHandler, \
    ReviewRequestedEventHandler, ReviewRequestRemovedEventHandler, ClosedEventHandler, EventHandler


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
