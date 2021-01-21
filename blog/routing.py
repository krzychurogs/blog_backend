from django.conf.urls import urls
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AlloweHostOriginValidator, OriginValidator

from chat.consumers import ChatConsumer
application=ProtocolTypeRouter({
	'websocket':AlloweHostOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				[
					url(r"^(?P<username>[\w.@+-]+)",ChatConsumer)
				]
				)
		)
	)
})