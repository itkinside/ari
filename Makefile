.PHONY: default clean

default:

clean:
	rm -f cache/*.pickle
	find . -type f -iname \*.pyc -delete
