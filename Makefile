celery-start:
	celery -A indel beat -l info
	celery -A indel worker -l info