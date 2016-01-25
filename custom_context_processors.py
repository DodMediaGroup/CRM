def usuario(request):
	try:
		nombre_usuario_sistema=request.user.first_name
		return {'nombre_usuario_sistema':nombre_usuario_sistema,'objeto_usuario':request.user}
	except Exception, e:
	#	raise e
		return {'nombre_usuario_sistema':''}
