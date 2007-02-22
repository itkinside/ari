.PHONY: default clean

default:

clean:
	rm -f cache/*
	find . -type f -iname \*.pyc -print0 | xargs -0 rm -f
