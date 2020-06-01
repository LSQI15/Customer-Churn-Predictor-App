clean:
	rm -r data
	mkdir data
	touch data/.gitkeep
	rm -r models
	mkdir models
	touch models/.gitkeep

data/raw.csv: config/config.yml
	python3 run.py download_data --config=config/config.yml
download: data/raw.csv

data/preprocessed.csv: config/config.yml
	python3 run.py preprocess_data --config=config/config.yml
preprocess: data/preprocessed.csv

data/featurized.csv: config/config.yml
	python3 run.py feaurize --config=config/config.yml
feature: data/featurized.csv

eda: config/config.yml
	python3 run.py eda --config=config/config.yml

random_forest: config/config.yml
	python3 run.py random_forest --config=config/config.yml

evaluate: config/config.yml
	python3 run.py evaluate_model --config=config/config.yml

create_db: config/.aws
	python3 run.py create_db

initial_ingest: config/.aws
	python3 run.py initial_ingest --config=config/config.yml

all_pipeline: clean download preprocess feature eda random_forest evaluate

.PHONY: download preprocess feature