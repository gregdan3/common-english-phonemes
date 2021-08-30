.PHONY: init run

init:
	pdm install
run:
	pdm run ./phonemes.py
