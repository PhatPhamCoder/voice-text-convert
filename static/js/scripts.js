async function convertTextToSpeech() {
  const text = document.getElementById("text-input").value;
  const response = await fetch("/api/text-to-speech", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  const data = await response.json();
  const audio = document.getElementById("audio-output");
  audio.src = "data:audio/mp3;base64," + data.audioContent;
}

async function convertSpeechToText() {
  const file = document.getElementById("audio-input").files[0];
  const reader = new FileReader();
  reader.onload = async function () {
    const audioContent = reader.result.split(",")[1];
    console.log({ audioContent });
    const response = await fetch("/api/speech-to-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ audioContent }),
    });
    const data = await response.json();
    document.getElementById("text-output").value =
      data.transcription || data.error;
  };
  reader.readAsDataURL(file);
}
