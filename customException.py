class FormValidation(Exception):

    def __init__(self, target, error):
        self.target = target
        self.error = error
        super().__init__(self.error)
