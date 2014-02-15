# -*- coding: utf-8 -*-

import json
from contextlib import closing

import unicodecsv


try:
	import cStringIO as StringIO
except ImportError:
	import StringIO


def filter_duplicate_params(params):
	for param in params:
		if param != "":
			return param


def filter_names(names):
	results = []
	for name in names:
		results.append(name.replace("_", " ").capitalize())
	return results


def json_to_csv(jsonData, fieldnames=None):
	"""
	Returns a CSV string from the given JSON data string.

	>>> import json
	>>> data = [
	... {"col1": "foo", "col2": "Ȓȳǡɴ"},
	... {"col1": "foo", "col2": "bar"},
	... {"col1": "foo", "col2": "bar"},
	... ]
	>>> csvData = json_to_csv(json.dumps(data))
	"""
	d = json.loads(jsonData)
	fieldnames = fieldnames or d[0].keys()
	return dict_to_csv(d, fieldnames)


def dict_to_csv(d, fieldnames):
	"""
	Returns a CSV string from the given list of dictionaries.

	This assumes that each dictionary is simple and each contains the same keys.

	>>> import json
	>>> data = [
	... {"col1": "foo", "col2": "Ȓȳǡɴ"},
	... {"col1": "foo", "col2": "bar"},
	... {"col1": "foo", "col2": "bar"},
	... ]
	>>> csvData = dict_to_csv(data, fieldnames=["col1", "col2"])
	"""
	buf = None
	with closing(StringIO.StringIO()) as f:
		dictWriter = unicodecsv.DictWriter(f, fieldnames)
		dictWriter.writeheader()
		dictWriter.writerows(d)

		buf = f.getvalue()

	return buf
