class Process:

    def __init__(self, source, output):
        self.source = source
        self.output = output

    def __call__(self):
        for source_thing in self.source.run():
            print(self.output.run())
