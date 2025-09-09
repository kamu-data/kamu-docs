.PHONY: dev
dev:
	hugo server -D -p 1414


.PHONY: dev-with-search
dev-with-search:
	@# TODO: Figure out how to run dev server with pagefind static files
	hugo -D
	npx -y pagefind --site public --serve


.PHONY: build
build: build-hugo build-pagefind

.PHONY: build-nix
build-nix:
	nix develop ./utilities/nix -c make build


.PHONY: build-hugo
build-hugo:
	HUGO_ENV=production hugo --minify


.PHONY: build-pagefind
build-pagefind:
	npx -y pagefind --site public


.PHONY: publish
publish: build
	aws s3 rm --recursive s3://docs.kamu.dev
	aws s3 cp public/ s3://docs.kamu.dev/ --recursive
	aws --no-cli-pager cloudfront create-invalidation --distribution-id E3LHDIU5YENQ3U --paths '/*'

.PHONY: publish-nix
publish-nix:
	nix develop ./utilities/nix -c make publish


.PHONY: docgen
docgen:
	python utilities/gen_reference.py > content/odf/reference.md
	python utilities/gen_glossary.py > content/glossary/_index.md
	python utilities/gen_spec.py > content/odf/spec.md
	python utilities/gen_rfcs.py content/odf/rfcs/
	python utilities/gen_cli_reference.py > content/cli/cli-reference.md


# Note this is an experimental Redoc rendering available under /node/api/rest/redoc/
# Our main renderer is based on Scalar and the instructions here:
#   https://github.com/scalar/scalar/blob/main/documentation/integrations/html.md
.PHONY: openapi
openapi:
	npx @redocly/cli build-docs ../kamu-node/resources/openapi-mt.json -o static/node/api/rest/redoc/index.html --title "Kamu Node REST API"


.PHONY: clean
clean:
	rm -rf public node_modules
