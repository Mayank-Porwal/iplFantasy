from app import create_app
from app import scheduler

if __name__ == '__main__':
    # with current_app.app_context():
    #     scheduler.add_job(
    #         id='submit',
    #         func=submit_all_teams_for_all_leagues,
    #         trigger='date',
    #         run_date='2024-03-21 18:57:55'
    #     )
    #     scheduler.start()
    context = create_app()
    scheduler.init_app(context)
    scheduler.start()
    context.run(debug=True, port=8000, use_reloader=False)
