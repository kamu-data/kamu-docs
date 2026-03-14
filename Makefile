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
	# python utils/gen_cli_commands_reference.py > content/cli/cli-reference.md
	# python utils/gen_cli_config_reference.py > content/cli/config-reference.md
	# python utils/gen_node_config_reference.py > content/node/config-reference.md


.PHONY: nix
nix:
	nix develop ./dev/nix
