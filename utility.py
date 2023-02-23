import requests as R
from bs4 import BeautifulSoup as BS
import json, logging

########################################
######## MAIN UTILITY FILE #############
########################################

# Configuring the log file
logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')


class tools:
    def get_response(self, url: str, *args, **kwargs) -> str:
        """Return a response object based on the input url.
        Arguments:
            * url -> URL of a website, example: 'https://wikipedia.com'"""
        
        try:
            response = R.get(url)
            logging.info('Ineuron GET Request')
        except ConnectionError:
            logging.error('Failed Ineuron Get Request')
            return 'Invalid URL'
        
        return response.text

    def html_parser(self, markup: str, *args, **kwargs) -> 'bs4.BeautifulSoup':
        """Return a bs4.BeautifulSoup object.
        Arguments:
            * markup -> A string consists of HTML tags"""
        
        return BS(markup, 'html.parser')

    def html_tag_finder(self, parsed_html: 'bs4.BeautifulSoup', tag_name: str, identifier: dict, *args, **kwargs) -> 'list[bs4.BeautifulSoup]':
        """Return a list of bs4.BeautifulSoup objects.
        Arguments:
            * parsed_html -> A Beautiful Soup Object
            * tag_name -> Name of HTML tag, like 'div', 'p'
            * identifier -> A dictonary containing id or class of HTML tag like {'class' : 'class_name'} or {'id' : 'id_name'}"""
        
        return parsed_html.findAll(tag_name, identifier)

    def convert_json(self, script_tags: 'list[str]', *args, **kwargs) -> dict:
        """Convert JSON written inside HTML script tags into Dictonary.
        Arguments:
            * script_tags -> A list of bs4.BeautifulSoup object containing HTML script tag."""

        JSON = ''
        for tags in script_tags:
            JSON += tags.text
        logging.info('Extracted JSON Data')
        return json.loads(JSON)



