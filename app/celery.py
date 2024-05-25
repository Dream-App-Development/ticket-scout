from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'run-playwright-task-every-hour': {
        'task': 'tasks.run_playwright_task',
        'schedule': 120.0,  # Run every hour
    },
}

app.conf.timezone = 'UTC'
