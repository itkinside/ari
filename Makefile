.PHONY: default clean

default:

clean:
	rm -f cache/*
	find . -type f -iname \*.pyc -delete
