from .base import OutputBase

class NullOutput(OutputBase):

    def __call__(self, file):
        pass

    def finalize(self):
        pass
