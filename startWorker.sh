export C_FORCE_ROOT="true"
python3 -m celery -A 'AutoScanWorker' worker --events
