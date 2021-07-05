.PHONY: clean pip-compile-dev pip-compile update-env run-app clean activate-env init isort black flake8 lint

#################################################################################
# GLOBALS                                                                       #
#################################################################################

SHELL=/bin/bash

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = streamlit-urbana
PACKAGE_NAME = streamlit-urbana
ENV_NAME = streamlit-urbana
SRC_CODE_FOLDER = streamlit-urbana
PYTHON_INTERPRETER = python
PORT = 8889

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## activate venv
activate-venv:
	source activate $(ENV_NAME)

## init development tools
init: activate-venv
	$(PYTHON_INTERPRETER) -m pip install pip-tools

## run app
run-app: activate-env
	streamlit run app.py --server.port $(PORT)

## Delete all compiled Python files
clean:
	find . -name "*.py[co]" -exec rm {} \;

## generate requirements-dev.txt
pip-compile-dev: requirements-dev.in activate-venv
	pip-compile requirements-dev.in

## generate requirements.txt
pip-compile: requirements.in activate-venv
	pip-compile requirements.in

## update environment
update-env: pip-compile-dev pip-compile activate-venv
	pip-sync requirements.txt requirements-dev.txt

## sort imports
isort:
	isort .

## prettify code with black
black:
	black .

## run the flake8 tool
flake8:
	flake8 .

## linter
lint: flake8 isort black

## bump version
bump-version: activate-env
	cz bump --changelog


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
