import asyncio
import websockets
import pyaudio
from transcribe import transcribe_audio

# WebSocket server configuration
HOST = 'localhost'
PORT = 8000

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Audio stream callback
def audio_callback(in_data, frame_count, time_info, status):
    text = transcribe_audio(in_data)
    print("Transcription:", text)  # Replace with your desired logic to handle transcriptions
    return None, pyaudio.paContinue

# WebSocket handler
async def handle_websocket(websocket, path):
    # Open PyAudio stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=audio_callback
    )

    try:
        while True:
            print("running")
            await asyncio.sleep(1)  # Keep the connection alive
    except websockets.exceptions.ConnectionClosedError:
        pass

    # Clean up resources
    stream.stop_stream()
    stream.close()
    p.terminate()

# Start WebSocket server
start_server = websockets.serve(handle_websocket, HOST, PORT)
print(1)
# Run the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()