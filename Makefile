.PHONY: default clean distclean

default:

clean:
	rm -f cache/*.pickle
	find . -type f -iname \*.pyc -delete

distclean: clean
	rm -rf build/ dist/ MANIFEST
