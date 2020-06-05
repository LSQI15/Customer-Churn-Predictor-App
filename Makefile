clean:
	rm -f data/*
	rm -f models/*

data/raw.csv: config/config.yml
	python3 run.py download_data --config=config/config.yml
download: data/raw.csv

data/preprocessed.csv: config/config.yml data/raw.csv
	python3 run.py preprocess_data --config=config/config.yml
preprocess: data/preprocessed.csv

data/featurized.csv: config/config.yml data/preprocessed.csv
	python3 run.py feaurize --config=config/config.yml
feature: data/featurized.csv

eda: config/config.yml data/preprocessed.csv data/featurized.csv
	python3 run.py eda --config=config/config.yml

random_forest: config/config.yml data/featurized.csv
	python3 run.py random_forest --config=config/config.yml

evaluate: config/config.yml models/predictions.csv
	python3 run.py evaluate_model --config=config/config.yml

unit_test:
	py.test

reproducibility_test: test/reproducibility_test_config.yml
	python3 run.py run_reproducibility_tests --config=test/reproducibility_test_config.yml

all_pipeline: clean download preprocess feature eda random_forest evaluate

.PHONY: download preprocess feature test reproducibility_test