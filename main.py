from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Lista para almacenar las conexiones WebSocket activas
active_connections = []

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Añadir conexión WebSocket a la lista de conexiones activas
    await websocket.accept()
    active_connections.append(websocket)
    print(active_connections, type(active_connections))
    try:
        while True:
            data = await websocket.receive_text()
            # Enviar mensaje a todos los clientes conectados
            for connection in active_connections:
                print(connection, data)
                await connection.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        # Cuando se desconecte, quitar la conexión de la lista
        active_connections.remove(websocket)
