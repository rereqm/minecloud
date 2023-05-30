
from main.models import Server
servers = Server.objects.all()
for server in servers:
    server.remaining_days-=1
    if server.remaining_days == 0 or server.remaining_days == -1:
        server.remaining_days = 0
        server.paid = False
    server.save()