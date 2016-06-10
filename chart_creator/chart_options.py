

class ChartOptions:
    """
    Similar to a Django Form class. Defines input fields that can be set by the
    user in the chart admin.

    ```
    options = ChartOptions({'key': 123})
    if options.is_valid():
        do_stuff(options.data)
    else:
        oh_no(options.errors)
    ```
    """
    def __init__(self, data):
        self._data = data
        self._cleaned_data = {}
        self._validated = False
        self.errors = None

    @property
    def data(self):
        """
        Get access to the
        :return:
        """
        if self.is_valid():
            return self._cleaned_data
        return None

    def validate(self):
        """
        Run validation against all the fields.
        :return:
        """
        self._validated = True

    def is_valid(self):
        """
        Test if the provided inputs are valid.
        :return: boolean
        """
        if not self._validated:
            self.validate()

        return self.errors is None
