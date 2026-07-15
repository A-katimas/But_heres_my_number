PYTHON		= uv run python3
UV			= uv
VENV		= .venv
SRC			= src
TMP_DIRS	= __pycache__ .mypy_cache .ruff_cache


install:
	@echo ">>> Installation de uv..."
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo ">>> Sync des dépendances (prod + dev)..."
	$(UV) sync
	@echo ">>> OK — projet prêt !"


run:
	@echo ">>> Lancement de la simulation..."
	$(PYTHON) -m $(SRC)


debug:
	@$(PYTHON) -m pdb -m $(SRC)

lint:
	@uv run $(PYTHON) -m flake8 . --max-line-length=79 --extend-exclude .venv
	@uv run $(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: lint

clean:
	@echo ">>> Suppression des fichiers temporaires..."
	rm -rf $(TMP_DIRS)
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -delete
	@echo ">>> Clean OK !"

fclean: clean
	@echo ">>> Suppression du venv..."
	@rm -rf $(VENV)
	@rm -rf uv.lock
	@echo ">>> FClean OK !"

.PHONY: run install debug clean fclean lint lint-strict