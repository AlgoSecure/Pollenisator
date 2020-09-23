export C_FORCE_ROOT="true"
celery -A 'AutoScanWorker' worker --events
