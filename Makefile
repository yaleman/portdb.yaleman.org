ZOLA ?= zola

.PHONY: build check generate serve

build:
	$(ZOLA) build

check:
	$(ZOLA) check --skip-external-links

generate:
	uv run python generatecontent.py

serve:
	$(ZOLA) serve --interface 127.0.0.1 --port 1111 --output-dir output --force
