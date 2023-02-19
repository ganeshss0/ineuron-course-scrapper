import requests as R
from bs4 import BeautifulSoup as BS
import json, logging


logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')


class tools:
    def get_response(self, url: str, *args, **kwargs) -> str:
        try:
            response = R.get(url)
            logging.info('Ineuron GET Request')
        except ConnectionError:
            logging.error('Failed Ineuron Get Request')
            return 'Invalid URL'
        
        return response.text

    def html_parser(self, markup: str, *args, **kwargs) -> 'bs4.BeautifulSoup':
        return BS(markup, 'html.parser')

    def html_tag_finder(self, parsed_html: 'bs4.BeautifulSoup', tag_name: str, identifier: dict, *args, **kwargs) -> 'list[bs4.BeautifulSoup]':
        return parsed_html.findAll(tag_name, identifier)

    def convert_json(self, script_tags: 'list[str]', *args, **kwargs) -> dict:
        
        '''Convert JSON written inside HTML script tags into Dictonary.'''

        JSON = ''
        for tags in script_tags:
            JSON += tags.text
        logging.info('Extracted JSON Data')
        return json.loads(JSON)



