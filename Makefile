.PHONY: default clean

default:

clean:
	rm -rf cache/*
	find . -type f -iname \*.pyc -print0 | xargs -0 rm -rf
