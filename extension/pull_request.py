class PullRequest(object):
    def __init__(self):
        self.repo_name = ''
        self.action = ''
        self.number = 0
        self.by = ''
        self.state = ''
        self.title = ''
        self.url = ''
        self.assignee = ''
        self.requested_reviewers = []
        self.removed_reviewer = ''
        self.label = ''
        self.is_merged = False
        self.merged_by = ''
        self.merged_at = ''
        self.comment = ''

    # def __setattr__(self, key, value):
    #     if key in self:
    #         self.key = value
    #
    #     return self

    def __str__(self):
        return 'repo_name => {} - action => {} - number => {} - by => {} - state => {} - title => {} - url => {} ' \
               '- assignee => {} - reviewers => {} - removed_reviewer => {} - label => {} - comment - {} ' \
               '- is_merged => {} - merged_by => {} - merged_at => {}'.format(self.repo_name, self.action, self.number,
                                                                              self.by,
                                                                              self.state, self.title, self.url,
                                                                              self.assignee,
                                                                              self.requested_reviewers,
                                                                              self.removed_reviewer,
                                                                              self.label, self.comment, self.is_merged,
                                                                              self.merged_by, self.merged_at)
