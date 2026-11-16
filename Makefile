PYTHON ?= python3
HUGO ?= hugo

.PHONY: site site-serve

website/themes/blowfish/theme.toml:
	git submodule update --init --depth 1 website/themes/blowfish

site: website/themes/blowfish/theme.toml
	$(PYTHON) scripts/prepare_site.py
	$(HUGO) --source website --minify --cleanDestinationDir --panicOnWarning
	$(PYTHON) scripts/check_site.py

site-serve: website/themes/blowfish/theme.toml
	$(PYTHON) scripts/prepare_site.py
	$(HUGO) server --source website --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/ --renderToMemory
