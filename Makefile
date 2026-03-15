.PHONY: dev
dev:
	npx mint dev


.PHONY: lint
lint:
	npx mint broken-links


.PHONY: docgen
docgen:
	python utils/gen_reference.py > odf/reference.md
	python utils/gen_glossary.py > glossary.md
	python utils/gen_spec.py > odf/spec.md
	python utils/gen_rfcs.py odf/rfcs/
	python utils/gen_cli_commands_reference.py > cli/commands.md
	python utils/gen_cli_config_reference.py > cli/config.md
	python utils/gen_node_config_reference.py > node/config.md


.PHONY: nix
nix:
	nix develop ./dev/nix


.PHONY: clean
clean:
	rm -rf node_modules
