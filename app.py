from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as BS
import json
from utility import tools
from handle_mongo import Store_Mongo
from handle_sql import Store_Sql
from handle_pdf import create_pdf
import logging


##############################################
########## MAIN APPLICATION FILE #############
##############################################

class Scrapper(tools):
    """Main Data Scrapper"""
    # Keys 
    KEY_1 = 'props'
    KEY_2 = 'pageProps'
    KEY_3 = 'initialState'

    def __init__(self, url: str) -> None:
        self.URL = url

    def store_json(self, data: dict) -> None:
        """Stores a python dictonary object into a json file(data.json)."""
        
        with open('data.json', 'w') as File:
            json.dump(data, File)
        logging.info('Created data.json')

    def extract_clean_detail(self, data: dict) -> dict:
        """Return a dictonary after cleaning the input dictonary object."""
        
        # Try to get the values of classtimings
        try:
            timings = data['classTimings']['timings']
        except:
            timings = None
            
        # Try to get the values of course overview
        try:
            courseMeta = data['courseMeta'][0]['overview']
        except:
            courseMeta = None
            
        # Try to get the values of instructor details
        try:
            instructor = data['instructorsDetails']
        except:
            instructor = None
        
   
        return {
        'title' : data.get('title'),
        'description' : data.get('description'), 
        'Timings' : timings, 
        'lang' : courseMeta['language'],
        'learn' : courseMeta['learn'],
        'requirements' : courseMeta['requirements'],
        'features' : courseMeta['features'],
        'instructor' : instructor}



    def data_solver(self, data: dict) -> dict:
        """Return a dictonary object.\n
        Arguments:
            * data -> A dictonary of iNeuron.ai/courses raw json data.\n
        solved_data Dictonary Structure:\n
        {
            {'bundle_name' : {
                            'feature' : list[str],
                            'description' : list[str],
                            'courses' : list[dict],
                            'liveCourses' : list[dict],
                            'bundle_name' : str}},
                            ...}"""
        
        # Accessing the main part of dictonary
        data = data[self.KEY_1][self.KEY_2][self.KEY_3]
        solved_data = {}
        bundled = set()

        for bundle_name, bundle in data['bundles']['bundles'].items():
            solved_data[bundle_name] = {
                'feature' : bundle.get('features'),
                'description' : bundle.get('description').split(','),
                'courses' : [],
                'liveCourses' : [],
                'bundle_name' : bundle_name
            }
            for course in data['filter']['initCourses']:
                
                
                if (key:=course['_id']) in bundle['courses']:
                    bundled.add(key)
                    clean_course = self.extract_clean_detail(course)
                    solved_data[bundle_name]['courses'].append(clean_course)

                elif key in bundle['liveCourses']:
                    bundled.add(key)
                    clean_course = self.extract_clean_detail(course)
                    solved_data[bundle_name]['liveCourses'].append(clean_course)

        solved_data['Other Courses'] = {'courses' : [], 'bundle_name' : 'Others Courses', 'liveCourses': [], 'description':['Other Courses'], 'feature':['Courses']}
        for course in data['filter']['initCourses']:
            if not course['_id'] in bundled:
                solved_data['Other Courses']['courses'].append(self.extract_clean_detail(course))

        return solved_data
    
    @staticmethod
    def get_data() -> dict:
        '''Return a dictonary object.\n
        If the data if stored locally then it load the data into a python dictonary object.\n
        If not then it download the data.'''
        
        try:
            with open('./data.json') as File:
                data = json.load(File)
        except:
            data = get_bundles(return_data = True)
        return data
                    


    
# Initial the Flask app
app = Flask(__name__)
CORS(app)

# Configuring the log file
logging.basicConfig(filename = 'app.log', filemode='a', level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s')


# Adding the homepage route method
@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def homepage():
    """Return a render_template object."""
    
    logging.info('Home Page Rendered')
    return render_template('index.html')


# Adding the /bundles page route method
@app.route('/bundles', methods = ['GET', 'POST'])
@cross_origin()
def get_bundles(return_data = False):
    # Creating a instance of Scrapper class with a url
    scrap = Scrapper('https://ineuron.ai/courses')
    
    # Getting a reponse object
    response = scrap.get_response(url = scrap.URL)

    parsed_html = scrap.html_parser(markup = response)
    
    # Finding the script tag containing json data.
    course_data_tag = scrap.html_tag_finder(parsed_html = parsed_html, tag_name = 'script', identifier = {'id' : '__NEXT_DATA__'})

    data = scrap.convert_json(script_tags = course_data_tag)

    solved_data = scrap.data_solver(data)
    scrap.store_json(data = solved_data)
    
    if return_data:
        return solved_data
    logging.info('Bundle Page Rendered')
    return render_template('course_bundle.html', bundles = solved_data)
    

# Adding the /course page route method
@app.route('/course', methods = ['POST'])
@cross_origin()
def get_course():
    data = Scrapper.get_data()
    course_detail = request.form['course']
    bundle_name, section, course_name = course_detail.split('-')
    for course in data[bundle_name][section]:
        if course['title'] == course_name:
            logging.info('Course Page Rendered')
            return render_template('course.html', course = course)

    logging.warning('Failed to Fetch Course Data')
    return '<h1>Course is Not Available</h1>'

# Adding the /courses page route method
@app.route('/courses', methods = ['POST'])
@cross_origin()
def get_bundle_courses():
    bundle_name = request.form['Bundle']
    data = Scrapper.get_data()
    courses = data[bundle_name]
    logging.info('Rendered Courses Page')
    return render_template('courses.html', courses = courses, bundle_name = bundle_name)

# Adding the /raw page route method
@app.route('/raw', methods = ['GET', 'POST'])
@cross_origin()
def download():
    data = Scrapper.get_data()
    logging.info('Download Request')
    return jsonify(data)

# Adding the /mongo page route method
@app.route('/mongo', methods = ['GET', 'POST'])
@cross_origin()
def mongoPage():
    logging.info('Rendered Mongo Page')
    return render_template('mongo.html')

# Adding the /sql page route method
@app.route('/sql', methods = ['GET', 'POST'])
@cross_origin()
def sqlPage():
    logging.info('Rendered SQL Page')
    return render_template('sql.html')

# Adding the /result page route method
@app.route('/result', methods = ['POST'])
@cross_origin()
def save_to_db():
    db_name = request.form['DB']
    data = Scrapper.get_data()

    if db_name == 'mongo':
        connection = request.form['connection_string']
        connect = Store_Mongo(connection)
        if connect.test():
            if connect.upload(data):
                return '<h1>Successful</h1>'
            else:
                return '<h1>Failed</h1>'
        else:
            return '<h1>Invalid Credentials</h1>'


    elif db_name == 'sql':
        server = request.form['server']
        port = request.form['port']
        database = request.form['database']
        user = request.form['user']
        password = request.form['password']
        connect = Store_Sql(server, database, user, password, port)
        if connect.test():
            if connect.upload(data):
                return '<h1>Successful</h1>'
            else:
                return '<h1>Failed</h1>'
        else:
            return '<h1>Invalid Credentials</h1>'

# Adding the /PDF page route method
@app.route('/PDF', methods = ['GET', 'POST'])
@cross_origin()
def get_pdf():
    try:
        data = Scrapper.get_data()
        pdf = create_pdf()
        pdf.pdf(data)
        return send_file('data.pdf')
    except:
        logging.error('Unable to Create PDF')
        return '<h1>Unable to Create PDF File</h1>'
    




if __name__ == '__main__':
    logging.info('App Started')
    app.run(host = '0.0.0.0')                  # App started

