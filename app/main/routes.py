from flask import Blueprint, render_template

main = Blueprint('main', __name__)

fantasies = [
    {
        'type': 'Draft',
        'desc': 'Draft type',
        'content': 'play draft',
        'author': 'Maya',
        'date_posted': 'Jun 4, 2023'
    },
    {

        'type': 'Daily',
        'desc': 'Daily type',
        'content': 'play Daily',
        'author': 'test1',
        'date_posted': 'Jun 5, 2023'
    },
    {
        'type': 'League',
        'desc': 'League type',
        'content': 'play League',
        'author': 'test1',
        'date_posted': 'Jun 6, 2023'
    },
]


@main.route('/')
def home():
    return render_template('home.html', fantasies=fantasies)


@main.route('/about')
def about():
    return render_template('about.html', title='About Us')

