from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib

data_df = pd.read_excel('Preprocessed & Combined/Combined.xlsx')
data_df.dropna(axis=0, inplace=True)

universities = ['Arizona State University', 'Boston University', 'Georgia Institute of Technology',
                'New Jersey Institute of Technology', 'University of North Carolina', 'North Carolina State University',
                'New York University', 'Purdue University', 'University of California', 'University of Cincinnati',
                'University of Texas', 'University of South Florida', 'University of Maryland',
                'Carnegie Mellon University',
                'Texas A&M University', 'University of Illinois', 'University at Buffalo', 'Columbia University',
                'University of Washington', 'University of Michigan', 'Northeastern University']

specialization = ['Computer Science and Engineering', 'Computer Engineering Electrical Engineering',
                  'Computer Science Big Data Systems', 'Computer Science', 'Mechnical Engineering',
                  'Computer Engineering Computer Systems', 'Information Systems Management', 'Software Engineering',
                  'Cybersecurity', 'Computer Science (Software Engineering)',
                  'Robotics and Autonomous Systems', 'Robotics and Autonomous Systems Artificial Intelligence',
                  'Robotics and Autonomous Systems Mechanical and Aerospace Engineering',
                  'Civil Engineering (MSc)', 'Electrical Engineering', 'Construction Management',
                  'Computer Engineering',
                  'Civil Engineering', 'Electronic and Electrical Engineering MEng',
                  'Information Technology', 'Industrial Engineering', 'Construction Management and Technology',
                  'Aerospace Engineering', 'Business Analytics MS', 'Electrical & Electronic Engineering',
                  'Computer Science (Advanced)', 'Mechanical Engineering', 'Computer Science (Big Data)',
                  'Computer Science (Algorithms)', 'Business Analytics', 'Electrical and Electronics Engineering',
                  'Electrical and Computer Engineering', 'Information Systems (MIS)', 'Management Information Systems',
                  'Chemical Engineering', 'Systems Engineering', 'Energy Systems Engineering',
                  'Computer Information Systems',
                  'City Planning', 'Computational Science and Engineering', 'Civil and Environmental Engineering',
                  'Data Analytics', 'Environmental Science', 'Data Science', 'Cyber Security and Privacy',
                  'Data Science (MSc)', 'Master of Engineering Management',
                  'Business Analytics and Information Systems',
                  'Cyber Security', 'Data Science and Business Analytics',
                  'Construction Management Facility Management',
                  'Energy Science', 'Electrical and Computer Engineering Communications',
                  'Computer Science Data Science',
                  'Master of Engineering Management with Industry', 'Robotics', 'Machine Learning and Computer Vision',
                  'Mechatronic and Robotic Engineeering', 'Management of Technology', 'Technology Management',
                  'Construction Engineering and Management', 'Engineering Management', 'Urban Planning', 'Mechatronics',
                  'Automobile Engineering', 'Aeronautics and Astronautics', 'Marketing Analytics', 'Food Science',
                  'Supply Chain Management (Logistics)', 'Finance and Business Analytics', 'Computer Science Honours',
                  'Information Systems', 'Artificial Intelligence', 'Computer Engineering and Data Science',
                  'Information Technology and Management', 'Electrical & Computer Engineering',
                  'Materials Science and Engineering', 'Business Analytics MSc',
                  'System Engineering and Engineering Management', 'Marketing MS',
                  'Supply Chain Management', 'Information Management and Technology',
                  'Business Administration Business Analytics', 'Finance',
                  'Management Science', 'Finance (MSc)', 'Finance MS',
                  'Transportation Engineering', 'Masters Information Systems',
                  'Telecommunication Engineering', 'Data Science and Analytics',
                  'Engineering Electrical and Computer',
                  'Computer and Electrical Engineering',
                  'Computer Science (Cyber Security)',
                  'Computer Vision, Robotics and Machine Learning', 'Biotechnology',
                  'Materials Science', 'Mechanical Engineering Thermofluids',
                  'Biomedical Engineering',
                  'Civil Engineering Geotechnical Engineering',
                  'Mechanical Engineering Manufacturing', 'Chemical Engineering MSc',
                  'Electronic and Computer Engineering', 'Engineering Science',
                  'Robotics Engineering', 'Environmental Engineering',
                  'Civil Engineering Construction Management',
                  'Structural Engineering', 'Mechanical and Aerospace Engineering',
                  'Information Management', 'Mechanical Engineering Automotive',
                  'Industrial Engineering and Operations Research',
                  'Computer Science Engineering', 'MS', 'Project Management',
                  'Comuputer Science', 'Cyber Physical Systems', 'Image Processing',
                  'Building Science and Green Building',
                  'Photonics and Optoelectronics', 'Data Analytics Engineering',
                  'Regulatory Affairs for Drugs, Biologics, and Medical Devices',
                  'Mathematical and Computational Science Engineering',
                  'Engineering Civil Engineering',
                  'Electrical Engineering Robotics and Computer Vision',
                  'Civil Engineering Construction Engineering and Management',
                  'Artificial Intelligence and Robotics',
                  'Mechanical Engineering Automation and Robotic Systems',
                  'Computer Science (Hons)', 'Industrial Design',
                  'Computer Science Software Engineering',
                  'Electrical Engineering Very Large Scale Integration Design',
                  'Biology', 'Engineering', 'Architecture',
                  'Mechanical Engineering with Robotics (with an industrial placement year)',
                  'Economics', 'Building Construction and Facility Management',
                  'Quantitative and Computational Finance',
                  'Applied Business Analytics', 'Automation and Robotic Systems',
                  'Advanced Computing (Machine Learning, Data Mining and High Performance Computing)',
                  'Technology, Cybersecurity and Policy', 'Pharmaceutical Chemistry',
                  'Applied Physics', 'Healthcare Administration',
                  'Emergency Management', 'Financial Mathematics',
                  'Data Science Computer Science', 'Forestry',
                  'Construction Technology',
                  'Robotics, Mechatronics and Control Engineering',
                  'Robotics and Mechatronics Engineering',
                  'Cybersecurity Engineering', 'Biotechnology and Entrepreneurship',
                  'Statistics', 'Biochemical Engineering',
                  'Construction Project Management', 'Computer Systems',
                  'Computer Science Artificial Intelligence',
                  'Computer Science with Data Science', 'Product Management',
                  'Computational Data Science',
                  'Computing (Artificial Intelligence and Machine Learning)',
                  'Biotechnology and Bioengineering',
                  'Electronics and Communication Engineering',
                  'Business Administration Management Information Systems',
                  'Electronics and Instrumentation Engineering',
                  'Exercise Sci/Kinesiology', 'Public Health Administration',
                  'Data Science and Engineering',
                  'Civil Engineering: Environmental and Water Resources Engineering',
                  'Applied Data Science', 'Business', 'Software Systems Engineering',
                  'Business Intelligence/Data Analytics', 'Health Informatics',
                  'Environmental Resources Engineering', 'Bioengineering',
                  'Bioinformatics', 'Civil and Structural Engineering']

exam = ['IELTS', 'TOEFL']
uni_list = list(np.sort(data_df['University'].unique()))
data_df['Specialization'] = data_df['Specialization'].astype('str')
spec_list = list(np.sort(data_df['Specialization'].unique()))
exam_list = list(np.sort(data_df['Exam'].unique()))

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/analytics')
def analytics():
    return render_template("analytics.html")


@app.route('/predict', methods=["GET", "POST"])
def predict():
    probability = 0.0
    final_answer = ''
    input_df = pd.DataFrame(index=[0])
    if request.method == 'POST':
        input_df['Name'] = request.form.get('Name')
        input_df['CGPA'] = float(request.form.get('CGPA'))
        input_df['WorkExp(Years)'] = int(request.form.get('Work Exp')) % 12
        input_df['Research'] = int(request.form.get('Research'))
        input_df['Quant'] = int(request.form.get('Quant'))
        input_df['Verbal'] = int(request.form.get('Verbal'))
        input_df['AWA'] = float(request.form.get('AWA'))
        input_df['GRE'] = int(request.form.get('Quant')) + int(request.form.get('Verbal')) + float(request.form.get('AWA'))
        input_df['Speaking'] = float(request.form.get('Speaking'))
        input_df['Listening'] = float(request.form.get('Listening'))
        input_df['Writing'] = float(request.form.get('Writing'))
        input_df['Reading'] = float(request.form.get('Reading'))
        input_df['Score'] = float(request.form.get('Score'))

        for u in uni_list:
            if u == request.form.get('University'):
                input_df['University_' + u] = 1
            else:
                input_df['University_' + u] = 0
        for s in spec_list:
            if s == request.form.get('Specialization'):
                input_df['Specialization_' + s] = 1
            else:
                input_df['Specialization_' + s] = 0
        for e in exam_list:
            if e == request.form.get('Exam'):
                input_df['Exam_' + e] = 1
            else:
                input_df['Exam_' + e] = 0

        input_df.drop(['Name'], axis=1, inplace=True)
        # print(data_df.columns)
        # print(input_df.columns)
        xgb_predictor = joblib.load('XGBoost predictor.joblib')
        probability = np.squeeze(xgb_predictor.predict_proba(input_df))[1]
        final_answer = 'Your chance of getting admit is ' + str(np.round(probability, 2))

    return render_template("predict2.html",
                           universities=universities,
                           specialization=specialization,
                           exam=exam,
                           final_answer=final_answer)


if __name__ == '__main__':
    app.run(debug=True)
