DATA_PATH=data
CONFIG_PATH=config
MODEL_PATH=models
EDA_PATH=eda

clean:
	rm -rf ${DATA_PATH}
	mkdir ${DATA_PATH}
	touch ${DATA_PATH}/.gitkeep

	rm -rf ${MODEL_PATH}
	mkdir ${MODEL_PATH}
	touch ${MODEL_PATH}/.gitkeep

	rm -rf ${EDA_PATH}
	mkdir ${EDA_PATH}
	touch ${EDA_PATH}/.gitkeep

${DATA_PATH}/raw.csv: ${CONFIG_PATH}/config.yml
	python3 run.py download_data --file_path=${DATA_PATH}/raw.csv --config=${CONFIG_PATH}/config.yml
download: ${DATA_PATH}/raw.csv

${DATA_PATH}/preprocessed.csv: ${CONFIG_PATH}/config.yml ${DATA_PATH}/raw.csv
	python3 run.py preprocess_data --in_file_path=${DATA_PATH}/raw.csv --out_file_path=${DATA_PATH}/preprocessed.csv --config=${CONFIG_PATH}/config.yml
preprocess: ${DATA_PATH}/preprocessed.csv

${DATA_PATH}/featurized.csv: ${CONFIG_PATH}/config.yml ${DATA_PATH}/preprocessed.csv
	python3 run.py featurize --in_file_path=${DATA_PATH}/preprocessed.csv --out_file_path=${DATA_PATH}/featurized.csv --config=${CONFIG_PATH}/config.yml
feature: ${DATA_PATH}/featurized.csv

eda: ${CONFIG_PATH}/config.yml ${DATA_PATH}/preprocessed.csv ${DATA_PATH}/featurized.csv
	python3 run.py eda --in_file_preprocessed=${DATA_PATH}/preprocessed.csv --in_file_featurized=${DATA_PATH}/featurized.csv --out_file_path=${EDA_PATH} --config=${CONFIG_PATH}/config.yml

random_forest: ${CONFIG_PATH}/config.yml ${DATA_PATH}/featurized.csv
	python3 run.py random_forest --in_file_path=${DATA_PATH}/featurized.csv --out_file_path=${MODEL_PATH} --config=${CONFIG_PATH}/config.yml

evaluate: ${CONFIG_PATH}/config.yml ${MODEL_PATH}/predictions.csv
	python3 run.py evaluate_model --in_file_path=${MODEL_PATH}/predictions.csv --out_file_path=${MODEL_PATH} --config=${CONFIG_PATH}/config.yml

unit_test:
	py.test

reproducibility_test: test/reproducibility_test_config.yml
	python3 run.py run_reproducibility_tests --config=test/reproducibility_test_config.yml

all_pipeline: clean download preprocess feature eda random_forest evaluate

.PHONY: download preprocess feature unit_test reproducibility_test