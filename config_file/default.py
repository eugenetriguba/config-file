class Default:
    """
    Default is used for the `default` value in ConfigFile's `get`.

    Previously, the default value for `get` was None. However, then
    the user cannot have `get` return a default value of None. So this
    class is used instead to get around that limitation.
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Default Value: {} ({})".format(self.value, type(self.value))
