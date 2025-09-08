
.PHONY : update_vendor_assets, tailwind, celery, run_simulations

DJANGO_READ_DOT_ENV_FILE=True
export

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

load_regions:
	python manage.py shell --command="from scripts import data_processing; data_processing.load_regions()"

load_data:
	python manage.py shell --command="from scripts import data_processing; data_processing.load_data()"

run_simulations:
	python manage.py shell -c "from scripts import data_processing as dp; dp.prerun_initial_myplan_scenario()"

celery:
	redis-server --port 6380 & celery -A config.celery_app worker -l INFO

tailwind:
	npx tailwindcss -i reenact/static/css/tailwind_input.css -o reenact/static/css/tailwind.css

update_vendor_assets:
	# Note: call this command from the same folder your Makefile is located
	# Note: this run only update minor versions.
	# Update major versions manually, you can use "ncu" for this.
	# https://nodejs.dev/en/learn/update-all-the-nodejs-dependencies-to-their-latest-version/#update-all-packages-to-the-latest-version

	# Update
	npm update

	# Ion.RangeSlider https://github.com/IonDen/ion.rangeSlider
	rm -r reenact/static/vendors/ionrangeslider/*
	cp node_modules/ion-rangeslider/js/ion.rangeSlider.min.js reenact/static/vendors/ionrangeslider/
	cp node_modules/ion-rangeslider/css/ion.rangeSlider.min.css reenact/static/vendors/ionrangeslider/

	# jQuery https://github.com/jquery/jquery
	rm -r reenact/static/vendors/jquery/*
	cp node_modules/jquery/dist/jquery.slim.min.* reenact/static/vendors/jquery/

	# eCharts https://echarts.apache.org/en/index.html
	rm -r reenact/static/vendors/echarts/*
	cp node_modules/echarts/dist/echarts.min.js reenact/static/vendors/echarts/

	# MapLibre GL JS https://github.com/maplibre/maplibre-gl-js
	rm -rf reenact/static/vendors/maplibre/js/*
	mkdir -p reenact/static/vendors/maplibre/js
	cp node_modules/maplibre-gl/dist/maplibre-gl.js reenact/static/vendors/maplibre/js/
	cp node_modules/maplibre-gl/dist/maplibre-gl.js.map reenact/static/vendors/maplibre/js/
	rm -rf reenact/static/vendors/maplibre/css/*
	mkdir -p reenact/static/vendors/maplibre/css
	cp node_modules/maplibre-gl/dist/maplibre-gl.css reenact/static/vendors/maplibre/css/

	# PubSubJS https://github.com/mroderick/PubSubJS
	rm -rf reenact/static/vendors/pubsub/js/*
	mkdir -p reenact/static/vendors/pubsub/js
	cp node_modules/pubsub-js/src/pubsub.js reenact/static/vendors/pubsub/js/

	# jQuery https://github.com/jquery/jquery
	rm -rf reenact/static/vendors/jquery/js/*
	mkdir -p reenact/static/vendors/jquery/js
	cp node_modules/jquery/dist/jquery.min.* reenact/static/vendors/jquery/js/
