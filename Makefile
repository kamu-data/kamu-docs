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
	aws --no-cli-pager cloudfront create-invalidation --distribution-id E3LHDIU5YENQ3U --paths '/*'

.PHONY: docgen
docgen:
	python utilities/gen_reference.py > content/odf/reference.md
	python utilities/gen_glossary.py > content/glossary/_index.md
	python utilities/gen_spec.py > content/odf/spec.md
	python utilities/gen_rfcs.py content/odf/rfcs/
	python utilities/gen_cli_reference.py > content/cli/cli-reference.md
