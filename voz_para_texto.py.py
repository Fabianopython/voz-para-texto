import sounddevice as sd
import wave
from openai import OpenAI
from gtts import gTTS
import pygame

# Configuração da API OpenAI
client = OpenAI(api_key="sua_api_key_aqui")

# Função para gravar áudio
def gravar_audio(nome_arquivo="entrada.wav", duracao=5, fs=16000):
    print("🎙️ Gravando...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
    sd.wait()
    with wave.open(nome_arquivo, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fs)
        f.writeframes(audio.tobytes())
    print("✅ Gravação concluída!")

# Função para tocar áudio com pygame
def tocar_audio(arquivo="resposta.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Função principal da conversa
def conversa():
    # 1. Gravar áudio
    gravar_audio()

    # 2. Transcrever com Whisper
    with open("entrada.wav", "rb") as f:
        transcricao = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    texto_usuario = transcricao.text
    print("📝 Você disse:", texto_usuario)

    # 3. Processar com ChatGPT
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": texto_usuario}]
    )
    texto_resposta = resposta.choices[0].message.content
    print("🤖 ChatGPT respondeu:", texto_resposta)

    # 4. Converter resposta em voz
    tts = gTTS(text=texto_resposta, lang="pt")
    tts.save("resposta.mp3")
    tocar_audio("resposta.mp3")

# Executar loop de conversa
if __name__ == "__main__":
    while True:
        conversa()
