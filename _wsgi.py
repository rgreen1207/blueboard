import cgi
from json import loads, dumps
from urllib import parse as urlparse

from api.request_management import RequestManagement
from gevent.pywsgi import WSGIServer


def parseAndDelistArguments(args): 
	if isinstance(args, (str, type(u""))) and args[:1] in ['{', '[']:
		args = loads(args)
		if isinstance(args, list): return args;
	else:
		args = urlparse.parse_qs(args)

	return delistArguments(args)


def delistArguments(args):
	'''
		Takes a dictionary, 'args' and de-lists any single-item lists then
		returns the resulting dictionary.
		{'foo': ['bar']} would become {'foo': 'bar'}
	'''
	
	def flatten(k,v):
		if len(v) == 1 and isinstance(v, list): return (str(k), v[0]);
		return (str(k), v)

	return dict([flatten(k,v) for k,v in args.items()])


def application(env, start_response):

	path = env['PATH_INFO']
	print('_wsgi.path(initial):', path)

	if path == '/':
		start_response('302 Moved Temporarily', [('Location', 'http://blueboard.com')])
		return ''

	if path == '/favicon.ico': 
		start_response('301 Moved Permanently', [('Location', 'http://blueboard.com/favicon.ico')])
		return ''
	
	path = path.split('/')
	version = path[1]
    
	if len(path) < 2 or path[1] != 'v1.0':
		start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
		return 'invalid API version'

	path = path[2:]
	if not path[-1]: path.pop();
	print('_wsgi.path(cleaned):', path)

	method = env['REQUEST_METHOD'].upper()
	print('method:', method)
	
	args = parseAndDelistArguments(env['QUERY_STRING'])
	print('args: ', args)

	wsgi_input = env['wsgi.input']

	if wsgi_input.content_length and method != 'PUT':
		print('wsgi_input: ', wsgi_input.content_length)
		post_env = env.copy()
		post_env['QUERY_STRING'] = ''
		form = cgi.FieldStorage(
			fp=env['wsgi.input'],
			environ=post_env,
			keep_blank_values=True
		)
		form_data = [(k, form[k].value) for k in form.keys()]
		args.update(form_data)

	if method == 'PUT':	
		wsgi_input = wsgi_input.read()
		args.update(parseAndDelistArguments(wsgi_input))

	#now call the methods as needed
	try:
		ret = { 
			'version': version,
			'path' : path,
			'args' : args,
			'method' : method,
			'response': RequestManagement(path, method, args).handle_request()
		}
		start_response('200 OK', [('Content-Type', 'application/json')])
		return {dumps(ret).encode('utf-8')}

	except Exception as inst:
		start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
		return repr(inst)


if __name__ == '__main__':
	wsgi_port = 8088
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), application).serve_forever()
