class SonderaError(Exception):
    """ General exception for sondera errors
    Attributes
    ----------
    message : str
        error message
    report_issue : bool
        flag for including reporting issue message
    issue_messages: list
        if report_issue, then provide details related to error
    """
    def __init__(self, message, report_issue=False, issue_messages=None):

        self.message = message

        if report_issue:
            append_message = ('\nPlease report to '
                              'https://github.com/rhkarls/sondera/issues '
                              'and include the error message above together with the '
                              'following information: \n')
            append_message += f'\nplaceholder_version_string' # TODO version: {fstring}
            if issue_messages is not None:
                append_message += '\n'
                for im in issue_messages:
                    append_message += f'{im=}\n'
            self.message += append_message


    def __str__(self):
        return f"{self.message}"

class APIError(Exception):
    """General exception API error

    Attributes
    ----------
    status_code : int
        status code from api
    message : str
        error message
    """

    def __init__(self, status_code, message):

        message_string = message.get("message", "Unknown error")

        self.status_code = status_code
        self.message = message_string

    def __str__(self):
        return f"{self.status_code}: {self.message}"
