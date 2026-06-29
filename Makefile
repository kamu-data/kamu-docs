.PHONY: nix
nix:
	nix develop ./utils/nix


.PHONY: dev
dev:
	npx mint dev


.PHONY: lint
lint:
	npx mint broken-links


.PHONY: docgen
docgen:
	python utils/gen_schemas.py > odf/schemas.md
	python utils/gen_glossary.py > general/glossary.md
	python utils/gen_spec.py > odf/spec.md
	python utils/gen_rfcs.py
	python utils/gen_cli_commands_reference.py > cli/commands.md
	python utils/gen_cli_config_reference.py > cli/config.md
	python utils/gen_node_config_reference.py > node/config.md


.PHONY: clean
clean:
	rm -rf node_modules
