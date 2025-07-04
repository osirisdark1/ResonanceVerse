# resonance_3d_visualizer.py
# Generates 3D resonance geometry for a given word based on Eric's custom math logic (1x1=2)
# BONUS MODE: Compares Genesis 1:1, Enoch 1:1, and Pyramid-coded word shapes
# VIDEO MODE: Plays each word in sequence with sound and 3D visual shape

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sounddevice as sd
import time
from resonant_math import word_to_frequency, word_to_angle, frequency_to_radius

# ------------------------------
# Generate 3D Standing Wave Shape
# ------------------------------
def generate_resonance_shape(freq, grid_size=50):
    x = np.linspace(-np.pi, np.pi, grid_size)
    y = np.linspace(-np.pi, np.pi, grid_size)
    z = np.linspace(-np.pi, np.pi, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    R = np.sqrt(X**2 + Y**2 + Z**2)
    field = np.sin(freq * R**2 / 1000)

    return X, Y, Z, field

# ------------------------------
# Visualize in 3D (isosurface style)
# ------------------------------
def visualize_3d_shape(X, Y, Z, field, threshold=0.5, title="3D Resonance Geometry"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)

    mask = np.abs(field) > threshold
    ax.scatter(X[mask], Y[mask], Z[mask], c=field[mask], cmap='plasma', alpha=0.6, s=2)

    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    plt.show(block=False)
    plt.pause(1.5)
    plt.close()

# ------------------------------
# Synthesize and play tone
# ------------------------------
def play_tone(freq, duration=1.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * freq * t)
    sd.play(waveform, samplerate=sample_rate)
    sd.wait()

# ------------------------------
# VIDEO MODE: Visual + Tone Sequence
# ------------------------------
def play_sequence(words):
    for word in words:
        fq = word_to_frequency(word)
        print(f"{word} → {fq:.2f} Hz")
        X, Y, Z, field = generate_resonance_shape(fq)
        play_tone(fq)
        visualize_3d_shape(X, Y, Z, field, title=f"{word} ({fq:.2f} Hz)")
        time.sleep(0.5)

# ------------------------------
# Main Execution
# ------------------------------
def render_word_shape(word):
    fq = word_to_frequency(word)
    print(f"Word: {word} → Frequency: {fq:.2f} Hz")
    X, Y, Z, field = generate_resonance_shape(fq)
    visualize_3d_shape(X, Y, Z, field, title=f"{word} ({fq:.2f} Hz)")

def compare_bonus_words():
    words = [
        ("Genesis", "Genesis 1:1"),
        ("Enoch", "Enoch 1:1"),
        ("Pyramid", "Pyramid Code")
    ]
    for word, source in words:
        fq = word_to_frequency(word)
        print(f"{source} → {word}: {fq:.2f} Hz")
        X, Y, Z, field = generate_resonance_shape(fq)
        visualize_3d_shape(X, Y, Z, field, title=f"{source} → {word} ({fq:.2f} Hz)")

if __name__ == '__main__':
    mode = input("Enter '1' for single word, '2' for bonus comparison, '3' for verse video playback: ")
    if mode.strip() == '1':
        test_word = input("Enter a word to render its 3D frequency shape: ")
        render_word_shape(test_word)
    elif mode.strip() == '2':
        compare_bonus_words()
    elif mode.strip() == '3':
        verse = input("Enter a sentence or verse to play word-by-word: ")
        words = verse.strip().split()
        play_sequence(words)