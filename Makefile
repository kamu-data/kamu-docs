.PHONY: dev
dev:
	npx mint dev

.PHONY: dev-nix
dev-nix:
	nix develop ./dev/nix -c npx mint dev
