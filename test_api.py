import base64
import msgpack
import requests

with open(
r"F:\pradhyumna_emirates_dub\voices\female_flight_attendant.wav",
"rb",
) as f:
audio_b64 = base64.b64encode(f.read()).decode()

payload = {
"text": "Welcome aboard Emirates.",
"format": "wav",
"references": [
{
"audio": audio_b64,
"text": "Welcome aboard Emirates."
}
]
}

r = requests.post(
"http://127.0.0.1:8080/v1/tts",
data=msgpack.packb(payload)
)

print(r.status_code)

with open("api_test.wav", "wb") as f:
f.write(r.content)

print("DONE")
