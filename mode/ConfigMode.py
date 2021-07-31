class ConfigItem():
    section = None
    option = None
    default = None
    restriction = None
    followup = None
    error_message = None

    def __init__(self, section, option, default, *, followup=None, restriction=None, error_message=None):
        self.section = section
        self.option = option
        self.default = default
        self.followup = followup
        self.restriction = restriction
        self.error_message = error_message

    def process_value(self, value):
        return_value = value
        if self.restriction:
            result = self.restriction(value)
            if not result:
                if self.error_message is not None:
                    raise ValueError(f"{self.error_message} {self.option}: [{value}]")
                else:
                    raise ValueError(f"Illegal value for {self.option}: [{value}]")
        if self.followup:
            return_value = self.followup(value)
        return return_value
