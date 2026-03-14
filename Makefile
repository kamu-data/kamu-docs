.PHONY: dev
dev:
	npx mint dev


.PHONY: lint
lint:
	npx mint broken-links


.PHONY: docgen
docgen:
	python utils/gen_reference.py > reference.md
	python utils/gen_glossary.py > glossary.md
	# python utilities/gen_spec.py > content/odf/spec.md
	# python utilities/gen_rfcs.py content/odf/rfcs/
	# python utilities/gen_cli_commands_reference.py > content/cli/cli-reference.md
	# python utilities/gen_cli_config_reference.py > content/cli/config-reference.md
	# python utilities/gen_node_config_reference.py > content/node/config-reference.md


.PHONY: nix
nix:
	nix develop ./dev/nix
