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


class Option:
    """
    Class representing elector API option object
    """

    def __init__(self, option_text: str, option_number: int = None, votes: int = None):
        self.__option_text = option_text
        self.__option_number = option_number
        self.__votes = votes

    @property
    def json(self) -> dict:
        """Returns dict (json) representing option"""
        json = {
            "option_number": self.__option_number,
            "option_text": self.__option_text,
            "votes": self.__votes,
        }

        return {key: value for key, value in json.items() if value != None}


class Question:
    """
    Class representing elector API question object
    """

    def __init__(self, question_text: str, options: [Option], question_number: str = None):
        self.__question_text = question_text
        self.__options = options
        self.__question_number = question_number

    @property
    def json(self) -> dict:
        """Returns dict (json) representing question"""

        json = {
            "question_number": self.__question_number,
            "question_text": self.__question_text,
            "options": [option.json for option in self.__options],
        }

        return {key: value for key, value in json.items() if value != None}


class Ballot:
    URL = "localhost:8000"

    def __init__(self, title: str, deadline: str, questions: [Question], voter_list: [str], **kwargs):
        self.__title = title
        self.__deadline = deadline
        self.__questions = questions
        self.__voter_list = voter_list
        self.__id = kwargs.get("id")
        self.__date_created = kwargs.get("date_created")

    @property
    def json(self) -> dict:
        json = {
            "id": self.__id,
            "title": self.__title,
            "date_created": self.__date_created,
            "deadline": self.__deadline,
            "questions": [question.json for question in self.__questions],
            "voter_list": self.__voter_list,
        }

        return {key: value for key, value in json.items() if value != None}
