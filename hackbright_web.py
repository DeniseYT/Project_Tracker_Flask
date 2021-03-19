"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student", methods=["GET"])
def get_student():
    """Show information about a student."""

    # get user input data
    # get a dict, key/value = 'github'/'jhacks'
    github = request.args.get('github')

    # connect hackbright_web.py(webpage route) & hackbright.py(SQLAlchemy)
    # call get_student_by_github to get the row
    first, last, github = hackbright.get_student_by_github(github)

    # feed data into template
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grade=grades)

    return html

    # github = "jhacks"
    # first, last, github = hackbright.get_student_by_github(github)
    # return "{} is the GitHub account for {} {}".format(github, first, last)


@app.route("/new-student")
def add_new_student():
    """Enters new student information"""

    return render_template('student_add.html')


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("added_student.html",
                        first_name=first_name,
                        last_name=last_name,
                        github=github)


@app.route("/project", methods=["GET"])
def get_project():
    """Show project"""

    title = request.args.get("title")

    title, description, max_grade = hackbright.get_project_by_title(title)
    grades = hackbright.get_grade_by_github_title(title)

    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            grades=grades)


@app.route("/")
def homepage():
    """This is homepage."""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html",
                            students=students,
                            projects=projects)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
