class Tree:

    def __init__(self):
        self.branch_list = []
        self.heads_list = []
        self.previous_branch = None
        self.last_br_id = 1
        branch = Branch(0)
        self.curr = branch  # current branch
        self.branch_list.append(branch)

    def new_branch(self):
        branch = Branch(self.last_br_id)
        self.last_br_id += 1
        self.curr.children.append(branch)
        self.previous_branch = self.curr
        self.curr = branch
        self.curr.parent = self.previous_branch
        if self.curr.parent.statement:
            self.curr.treepath.append(self.curr.parent.statement)
        self.branch_list.append(branch)
        return branch

    def parent(self):
        self.previous_branch = self.curr
        self.curr = self.curr.parent

    def get_branches(self):
        output = []
        for branch in self.branch_list:
            if type(branch) is not 'NoneType':
                output.append([branch, branch.parent, branch.treepath,
                               branch.children, branch.statement, branch.equals])
        return output


class Branch:

    def __init__(self, branch_id):
        self.parent = None
        self.children = []
        self.equals = []
        self.statement = None
        self.treepath = []  # full path from head to branch
        # self.name
        self.branch_id = branch_id

    def __repr__(self):
        return str(self.branch_id)
