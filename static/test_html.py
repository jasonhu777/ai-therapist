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
            <button disabled id="sendButton">Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("/start_session");
            ws.onmessage = function(event) {
                updateMessages(event.data, 'Assistant')
                document.getElementById("sendButton").disabled = false;
                
            };

            function updateMessages(message, sender = 'User') {
                var messages = document.getElementById('messages')

                const dividerNode = document.createElement('li')
                dividerNode.appendChild(document.createTextNode('--------------------'))
                
                const messageNode = document.createElement('li')
                console.log(message, sender)
                messageNode.appendChild(document.createTextNode(sender + ': ' + message))

                messages.appendChild(messageNode)
                messages.appendChild(dividerNode)
            }
            
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                updateMessages(input.value)
                input.value = ''
                document.getElementById("sendButton").disabled = true;
                
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""