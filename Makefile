.PHONY: default clean distclean

default:

clean:
	find . -type f -iname \*.pyc -delete

distclean: clean
	rm -rf build/ dist/ MANIFEST
