import requests as R
from bs4 import BeautifulSoup as BS
import json



class tools:
    def get_response(self, url: str, *args, **kwargs) -> str:
        try:
            response = R.get(url)
        except ConnectionError:
            return 'Invalid URL'
        
        return response.text

    def html_parser(self, markup: str, *args, **kwargs) -> 'bs4.BeautifulSoup':
        return BS(markup, 'html.parser')

    def html_tag_finder(self, parsed_html: 'bs4.BeautifulSoup', tag_name: str, identifier: dict, *args, **kwargs) -> 'list[bs4.BeautifulSoup]':
        return parsed_html.findAll(tag_name, identifier)

    def extract_links(self, tags: 'list[str]', baseurl: str, tag_identifier: str, *args, **kwargs) -> 'list[str]':
        return [baseurl + tag[tag_identifier] for tag in tags]

    def convert_json(self, script_tags: 'list[str]', *args, **kwargs) -> dict:
        
        '''Convert JSON written inside HTML script tags into Dictonary.'''

        JSON = ''
        for tags in script_tags:
            JSON += tags.text
        return json.loads(JSON)



