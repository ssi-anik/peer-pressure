class PullRequest(object):
    def __init__(self):
        self.number = 0
        self.title = ''
        self.repo = ''
        self.by = ''
        self.base = ''
        self.head = ''
        self.assignees = 'nobody'
        self.requested_reviewers = 'nobody'
        self.actor = 'someone'
        self.labels = ''
        self.is_merged = False
        self.merged_by = ''
        self.merged_at = ''
        self.comment = ''
        self.removed_reviewer = ''
        self.url = ''

        self.action = ''
        self.state = ''
        self.repo_url = ''

        self.actor_git_name = 'someone'
        self.by_git_name = ''
        self.removed_reviewer_git_name = ''
        self.assignees_array = []
        self.requested_reviewers_array = []

    def get_as_dict(self):
        return {
            'number': self.number,
            'title': self.title,
            'repo': self.repo,
            'by': self.by,
            'base': self.base,
            'head': self.head,
            'assignees': self.assignees,
            'requested_reviewers': self.requested_reviewers,
            'actor': self.actor,
            'labels': self.labels,
            'is_merged': self.is_merged,
            'merged_by': self.merged_by,
            'merged_at': self.merged_at,
            'comment': self.comment,
            'removed_reviewer': self.removed_reviewer,
            'url': self.url,
            'action': self.action,
            'state': self.state,
            'repo_url': self.repo_url,
        }

    def __str__(self):
        return 'number => {} - title => {} - repo => {} - by => {} - base => {} - head => {} - ' \
               'assignees => {} - requested_reviewers => {} - actor => {} - labels => {} - ' \
               'is_merged => {} - merged_by => {} - merged_at => {} - ' \
               'comment => {} - removed_reviewer => {} - url => {} - action => {} - ' \
               'state => {} - repo_url => {} - assignees_array => {} - ' \
               'requested_reviewers_array => {}'.format(self.number, self.title, self.repo,
                                                        self.by_git_name, self.base, self.head,
                                                        self.assignees,
                                                        self.requested_reviewers, self.actor_git_name,
                                                        self.labels, self.is_merged, self.merged_by,
                                                        self.merged_at, self.comment, self.removed_reviewer_git_name,
                                                        self.url, self.action, self.state,
                                                        self.repo_url, ", ".join(self.assignees_array),
                                                        ", ".join(self.requested_reviewers_array))
