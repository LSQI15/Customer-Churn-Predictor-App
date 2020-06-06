clean:
	rm -f data/*
	rm -f models/*

data/raw.csv: config/config.yml
	python3 run.py download_data --file_path=data --file_name=raw.csv --config=config/config.yml
download: data/raw.csv

data/preprocessed.csv: config/config.yml data/raw.csv
	python3 run.py preprocess_data --in_file_path=data --in_file_name=raw.csv --out_file_path=data --out_file_name=preprocessed.csv --config=config/config.yml
preprocess: data/preprocessed.csv

data/featurized.csv: config/config.yml data/preprocessed.csv
	python3 run.py feaurize --in_file_path=data --in_file_name=preprocessed.csv --out_file_path=data --out_file_name=featurized.csv --config=config/config.yml
feature: data/featurized.csv

eda: config/config.yml data/preprocessed.csv data/featurized.csv
	python3 run.py eda --in_file_path_preprocessed=data --in_file_name_preprocessed=preprocessed.csv --in_file_path_featurized=data --in_file_name_featurized=featurized.csv --out_file_path=models --config=config/config.yml

random_forest: config/config.yml data/featurized.csv
	python3 run.py random_forest --in_file_path=data --in_file_name=featurized.csv --out_file_path=models --config=config/config.yml

evaluate: config/config.yml models/predictions.csv
	python3 run.py evaluate_model --in_file_path=models --in_file_name=predictions.csv --out_file_path=models --config=config/config.yml

unit_test:
	py.test

reproducibility_test: test/reproducibility_test_config.yml
	python3 run.py run_reproducibility_tests --config=test/reproducibility_test_config.yml

all_pipeline: clean download preprocess feature eda random_forest evaluate

.PHONY: download preprocess feature unit_test reproducibility_test