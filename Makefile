
.PHONY : update_vendor_assets, tailwind, celery

DJANGO_READ_DOT_ENV_FILE=True
export

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

	# eCharts https://echarts.apache.org/en/index.html
#	rm -r digiplan/static/vendors/echarts/js/*
#	cp node_modules/echarts/dist/echarts.min.js digiplan/static/vendors/echarts/js/

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
