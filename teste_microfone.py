import sounddevice as sd

print("Gravando por 5 segundos...")
print("Fale normalmente!")

audio = sd.rec(
    int(5 * 48000),
    samplerate=48000,
    channels=1,
    dtype="int16",
    device=15
)

sd.wait()

print("Gravação terminou.")
print("Volume máximo:", abs(audio).max())