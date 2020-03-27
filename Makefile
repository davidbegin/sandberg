format:
	black music.py sandberg/*.py

t:
	python -m pytest tests/*.py
