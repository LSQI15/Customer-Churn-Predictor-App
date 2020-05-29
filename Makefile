clean:
	rm -r data
	mkdir data
	touch data/.gitkeep

data/raw.csv: config/config.yml
	python3 run.py download_data --config=config/config.yml
download: data/raw.csv

all_pipeline: clean download

.PHONY: download