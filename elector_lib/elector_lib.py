import requests
class AlreadyVotedException(Exception):
    """Already Voted Exception"""
    pass

class HaveNotVotedYetException(Exception):
    """Have Not Voted Yet Exception"""
    pass

class Vote():
    """ 
    :param url: URL for the new :class:`Vote` object.
    :param token: api_key
    :param ballot_id: ballot_id
    :param options: dictionary of answers of all questions
    """
    def __init__(self, url, token, ballot_id, options):
        self._url = url
        self._token = token
        self._ballot_id = ballot_id
        self._options = options
        self._voted = False

    def vote(self):
        """
        Sends vote request
        If you have already voted Raises AlreadyVotedException
        :rtype: requests.Response
        """
        
        if self._voted: raise AlreadyVotedException
        self._voted = True
        body = {"token": self._token, "ballot": self._ballot_id, "options": self._options}
        response = requests.post(f'http://{self._url}/ballot/api/vote/', json=body)
        self._status = response.status_code
        self._data = response.json()
        return response

    def status_code(self):
        """
        Returns response status code
        Raises HaveNotVotedYetException if you have not voted yet
        """
        if not self._voted: raise HaveNotVotedYetException
        return self._status

    def data(self):
        """
        Returns response data
        Raises HaveNotVotedYetException if you have not voted yet
        """
        if not self._voted: raise HaveNotVotedYetException
        return self._data