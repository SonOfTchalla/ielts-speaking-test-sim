const ws = new WebSocket("ws://localhost:8000/ws");

function sendMessage() {
    const message = document.getElementById("message").value;
    ws.send(message);
}

ws.onmessage = (event) => {
    document.getElementById("response").innerText = "Response: " + event.data;
};

async function uploadAudio() {
    const fileInput = document.getElementById("audioFile");
    if (fileInput.files.length === 0) {
        alert("Please select an audio file first.");
        return;
    }
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://localhost:8000/transcribe/", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    document.getElementById("transcription").innerText = "Transcription: " + data.transcript;

    const feedbackResponse = await fetch("http://localhost:8000/evaluate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: data.transcript })
    });
    const feedbackData = await feedbackResponse.json();
    document.getElementById("feedback").innerText = "Feedback: " + feedbackData.feedback;
}