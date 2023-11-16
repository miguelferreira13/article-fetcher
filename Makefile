.PHONY: build run save

build:
	docker build -t article-fetcher .

run:
	docker run --rm \
	-v $(PWD):/app \
	article-fetcher $(ARGS)

save:
	docker save -o article-fetcher.tar article-fetcher