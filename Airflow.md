# Airflow

## Key Objects

- DAG
- Task
- Operator
- Hook
- XCom

## Key Components

- **Webserver** - A Flask server running with Gunicorn that serves the Airflow UI.
- **Scheduler** - A Daemon responsible for scheduling jobs. This is a multi-threaded Python process that determines what tasks need to be run, when they need to be run, and where they are run.
- **Database** - A database where all DAG and task metadata are stored. This is typically a Postgres database, but MySQL, MsSQL, and SQLite are also supported.
- **Executor** - The mechanism for running tasks. An executor is running within the scheduler whenever Airflow is operational.
- **Worker** - The process that executes tasks, as defined by the executor. Depending on which executor you choose, you may or may not have workers as part of your Airflow infrastructure.

## Types of executors

- Sequential Executor
- Local Executor
- Celery Executor
- Kubernetes Executer


