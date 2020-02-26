from flask import render_template, url_for, flash, redirect, request
from ijazah_validation.forms import RecognitionForm
from ijazah_validation import app

from PIL import Image
from datetime import datetime

import os
import shutil
import ijazah_validation.functions as functions
import ijazah_validation.jpg_to_txt as jpg_to_txt
import ijazah_validation.validity_check_ijazah as vc_ijazah
import ijazah_validation.validity_check_ijazah as vc_ijazah

def find_the_highest_score(type, list, output_directory, name='', dob='', nik='', institution='', degree='', gpa='', english_score=''):

    # Initiate the dictionary result and other parameter
    result = {}
    first = True

    # list = functions.filter_list(list, type)
    
    # Loop through the given list and get the result, validity, and score
    for file in list:
        if type == 'akta':
            result_vc = vc_akta.main(output_directory + file, 'dictionary.json', name, date_of_birth)
        elif type == 'ktp':
            result_vc = vc_ktp.main(output_directory + file, name, dob, nik)
        elif type == 'ijazah':
            result_vc = vc_ijazah.main(output_directory + file, name, institution)
        elif type == 'transkrip':
            result_vc = vc_transkrip.main(output_directory + file, name, gpa)
        elif type == 'toefl':
            result_vc = vc_english_score.main(output_directory + file, name, english_score)

        # Check whether it is a first iteration, if it is so save it to result variable
        try:
            if first:
                result = result_vc
                first = False

            # If it is not the first iteration, we compare it to the highest score
            else:
                for key, value in result_vc.items():
                    if result_vc[key]['score'] > result[key]['score']:
                        result[key] = result_vc[key]
        except:
            return ''

    return result

def save_picture(ijazah):
    img = Image.open(ijazah)

    current_timestamps = datetime.now().strftime("%d%m%Y-%H%M%S")
    ijazah_fn = current_timestamps + '_' + 'ijazah.jpg'

    img.save(os.path.join(app.root_path, 'static', 'ijazah', ijazah_fn))

    return ijazah_fn

def clean_folder(folder='ijazah_validation/static/ijazah/'):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = RecognitionForm()

    if request.method == 'GET':
        image_file = url_for('static', filename='default.jpg')
        return render_template('home.html', form=form, image_file=image_file, input_data=None)

    elif request.method == 'POST':
        image_file = url_for('static', filename='default.jpg')

        if form.validate_on_submit():
            clean_folder()
            ijazah_file = save_picture(form.ijazah.data)
            image_file = url_for('static', filename='ijazah/'+ijazah_file)

            name = request.form['name']
            institution = request.form['institution']

            jpg_to_txt.main('ijazah_validation/static/ijazah/')

            input_data = {
                'name': name,
                'institution': institution 
            }

            list_of_txt_files = os.listdir('ijazah_validation/static/ijazah/output/')
            
            ijazah = find_the_highest_score('ijazah', list_of_txt_files, 'ijazah_validation/static/ijazah/output/', \
                                        name=name, \
                                        institution=institution)

            flash(f'Success', 'success')
            return render_template('home.html', form=form, image_file=image_file, input_data=input_data, recognition=ijazah)


        return render_template('home.html', form=form, image_file=image_file, input_data=None)