import os
import pyaudio
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from datetime import datetime

# Constants for Audio Processing
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 22050  # Sampling rate (matches Librosa's default)
CHUNK = 1024  # Buffer size

# Directory to Save Spectrograms
SAVE_PATH = r"C:\Users\apeksha narayan\Desktop\MINI_PROJECT\ai_model\real_time_spectrograms"
os.makedirs(SAVE_PATH, exist_ok=True)  # Create folder if it doesn't exist

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the Microphone Stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("🎤 Listening... Press Ctrl+C to stop.")

try:
    frame_count = 0
    while True:
        # Read audio data from stream
        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        audio_np = np.frombuffer(audio_data, dtype=np.int16)  # Convert to NumPy array
        
        # Normalize the audio
        audio_np = audio_np / np.max(np.abs(audio_np))

        # Compute Mel Spectrogram
        spectrogram = librosa.feature.melspectrogram(y=audio_np, sr=RATE)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        # Generate a unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_PATH, f"spectrogram_{frame_count}_{timestamp}.png")

        # Plot and Save Spectrogram
        plt.figure(figsize=(5, 4))
        librosa.display.specshow(spectrogram_db, sr=RATE, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"Real-Time Spectrogram {frame_count}")
        plt.tight_layout()
        
        plt.savefig(filename)  # Save spectrogram image
        plt.close()  # Close figure to free memory

        print(f"✅ Spectrogram saved: {filename}")
        frame_count += 1  # Increment frame count

except KeyboardInterrupt:
    print("\n🛑 Stopping Audio Stream...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("✅ Audio stream closed.")

