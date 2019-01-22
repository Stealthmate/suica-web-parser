exec:
	zip suicaParse.zip __main__.py suica.py
	echo '#!/usr/bin/env python3' | cat - suicaParse.zip > suicaParse
	chmod a+x suicaParse
	rm suicaParse.zip
