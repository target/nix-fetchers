import argparse


class BranchRevisionAction(argparse.Action):
    def __init__(self, nargs=None, **kwargs):
        if nargs != 2:
            raise ValueError("nargs must be 2")

        super(BranchRevisionAction, self).__init__(nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        branch = values[0]
        revision = values[1]

        self.validate_revision(revision)

        setattr(namespace, "branch", branch)
        setattr(namespace, "revision", revision)

    def validate_revision(self, rev):
        if len(rev) != 40:
            raise argparse.ArgumentError(
                self,
                "{} is not a valid Git revision: it must be 40 characters long".format(rev)   # noqa: E501
            )

        try:
            int(rev, 16)
        except ValueError as e:
            raise argparse.ArgumentError(
                self,
                "{} is not a valid Git revision: it isn't hexadecimal".format(rev)   # noqa: E501
            )
