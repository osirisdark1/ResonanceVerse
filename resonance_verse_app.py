# resonance_verse_app.py
# Resonance Verse: Full Sacred Tech Desktop App
# Uses resonant_math engine to decode scripture into sound + geometry

import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import os
import sys

# Try to import from resonant_math.py in the same directory, otherwise use mocks
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from resonant_math import word_to_frequency, word_to_angle, frequency_to_radius
except ImportError:
    # Mock implementations if resonant_math.py is missing
    def word_to_frequency(word):
        return 440 + (hash(word) % 200)  # Example: A4 + hash offset

    def word_to_angle(word):
        return (hash(word) % 360)  # Angle in degrees

    def frequency_to_radius(freq):
        return freq / 1000.0  # Example scaling

class ResonanceVerseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resonance Verse: Sacred Technology Engine")

        self.text_box = tk.Text(root, height=12, width=100)
        self.text_box.pack(pady=10)

        self.generate_btn = ttk.Button(root, text="Generate Geometry + Sound", command=self.run_engine)
        self.generate_btn.pack(pady=5)

        self.save_audio_btn = ttk.Button(root, text="Export WAV", command=self.save_audio)
        self.save_audio_btn.pack(pady=5)

        self.frequencies = []
        self.signal = None

    def run_engine(self):
        self.frequencies = []
        angles = []
        radii = []
        tones = []

        words = self.text_box.get("1.0", tk.END).split()
        for word in words:
            fq = word_to_frequency(word)
            angle = word_to_angle(word)
            radius = frequency_to_radius(fq)

            self.frequencies.append(fq)
            angles.append(np.radians(angle))
            radii.append(radius)
            tones.append(self.generate_tone(fq))

        self.signal = np.concatenate(tones)
        self.plot_geometry(angles, radii)

    def generate_tone(self, freq, duration=0.4, rate=44100):
        t = np.linspace(0, duration, int(rate * duration), endpoint=False)
        return 0.5 * np.sin(2 * np.pi * freq * t)

    def plot_geometry(self, angles, radii):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, radii, marker='o')
        ax.set_title("Sacred Frequency Geometry")
        plt.show()

    def save_audio(self):
        if self.signal is not None:
            path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
            if path:
                wav.write(path, 44100, (self.signal * 32767).astype(np.int16))

if __name__ == "__main__":
    root = tk.Tk()
    app = ResonanceVerseApp(root)
    root.mainloop()
