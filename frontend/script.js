const ws = new WebSocket("ws://localhost:8000/ws");

function sendMessage() {
    const message = document.getElementById("message").value;
    ws.send(message);
}

ws.onmessage = (event) => {
    document.getElementById("response").innerText = "Response: " + event.data;
};
