from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as BS
import requests
import json
from utility import tools
from handle_mongo import Store_Mongo
from handle_sql import Store_Sql

class Scrapper(tools):
    KEY_1 = 'props'
    KEY_2 = 'pageProps'
    KEY_3 = 'initialState'

    def __init__(self, url: str) -> None:
        self.URL = url

    def store_json(self, data: dict):
        with open('data.json', 'w') as File:
            json.dump(data, File)

    def extract_clean_detail(self, data: dict):
        try:
            timings = data['classTimings']['timings']
        except:
            timings = None
        try:
            courseMeta = data['courseMeta'][0]['overview']

        except:
            courseMeta = None
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



    def data_solver(self, data: dict):
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

        solved_data['Other Courses'] = {'courses' : [], 'course_link' : 'other_courses', 'liveCourses': []}
        for course in data['filter']['initCourses']:
            try:
                    timings = course.get('classTimings').get('timings')
            except:
                timings = None

            if not course['_id'] in bundled:
                solved_data['Other Courses']['courses'].append(self.extract_clean_detail(course))

        return solved_data
    
    @staticmethod
    def get_data():
        try:
            with open('./data.json') as File:
                data = json.load(File)
        except:
            data = get_bundles(return_data = True)
                    


    

app = Flask(__name__)
CORS(app)



@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def homepage():
    return render_template('index.html')



@app.route('/bundles', methods = ['GET', 'POST'])
@cross_origin()
def get_bundles(return_data = False):
    scrap = Scrapper('https://ineuron.ai/courses')

    response = scrap.get_response(url = scrap.URL)

    parsed_html = scrap.html_parser(markup = response)

    course_data_tag = scrap.html_tag_finder(parsed_html = parsed_html, tag_name = 'script', identifier = {'id' : '__NEXT_DATA__'})

    data = scrap.convert_json(script_tags = course_data_tag)

    solved_data = scrap.data_solver(data)
    scrap.store_json(data = solved_data)
    
    if return_data:
        return solved_data

    return render_template('course_bundle.html', bundles = solved_data)
    


@app.route('/course', methods = ['POST'])
@cross_origin()
def get_course():
    data = Scrapper.get_data()

    bundle_name, section, course_name = course_detail.split('-')
    for course in data[bundle_name][section]:
        if course['title'] == course_name:
            return render_template('course.html', course = course)

    return '<h1>Course is Not Available</h1>'

@app.route('/courses', methods = ['POST'])
@cross_origin()
def get_bundle_courses():
    bundle_name = request.form['Bundle']
    data = Scrapper.get_data()
    courses = data[bundle_name]
    return render_template('courses.html', courses = courses, bundle_name = bundle_name)

@app.route('/raw', methods = ['GET', 'POST'])
@cross_origin()
def download():
    data = Scrapper.get_data()
    return jsonify(data)


@app.route('/mongo', methods = ['GET', 'POST'])
@cross_origin()
def mongoPage():
    return render_template('mongo.html')


@app.route('/sql', methods = ['GET', 'POST'])
@cross_origin()
def sqlPage():
    return render_template('sql.html')

@app.route('/sql', methods = ['GET', 'POST'])
@cross_origin()
def save_to_db():
    db_name = request.form['DB']
    data = Scrapper.get_data()

    if db_name == 'mongo':
        connection = request.form['connection_string']
        connect = Store_Mongo(connection)
        if connect.test():
            result = connect.upload(data)
            return '<h1>' + result + '</h1>'
        else:
            return '<h1>Invalid Credentials</h1>'


    elif db_name == 'sql':
        server = request.form['server']
        database = request.form['database']
        user = request.form['user']
        password = request.form['password']
        connect = Store_Sql(server, database, user, password)
        if connect.upload(data):
            return '<h1>Data Saved Successfull</h1>'
        else:
            return '<h1>Invalid Credentials</h1>'

    
    




if __name__ == '__main__':
    app.run(host = '0.0.0.0')
