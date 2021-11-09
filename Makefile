.PHONY: dev
dev:
	hugo server -D

.PHONY: build
build:
	HUGO_ENV=production hugo

.PHONY: publish
publish: build
	aws s3 rm --recursive s3://docs.kamu.dev
	aws s3 cp public/ s3://docs.kamu.dev/ --recursive
	aws cloudfront create-invalidation --distribution-id E3LHDIU5YENQ3U --paths '/*'
