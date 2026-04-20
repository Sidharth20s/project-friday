"""
FRIDAY AI Assistant — Voice Engine
Handles Speech Recognition (STT) and Text-to-Speech (TTS).
"""

import threading
import queue
import time
import pyttsx3
import speech_recognition as sr
from assistant.config import WAKE_WORD, VOICE_SPEED, VOICE_VOLUME


import threading
import queue
import time
import io
import wave
import numpy as np
import sounddevice as sd
import pyttsx3
import speech_recognition as sr
from assistant.config import WAKE_WORD, VOICE_SPEED, VOICE_VOLUME


class VoiceEngine:
    def __init__(self, on_command_callback=None):
        self.on_command = on_command_callback
        self.is_listening = False
        self.is_speaking = False
        self.wake_word = WAKE_WORD.lower()
        self.recognizer = sr.Recognizer()
        self.tts = None
        self.active = False
        
        # Audio settings
        self.sample_rate = 16000
        self.channels = 1
        self.energy_threshold = 300 # Default SR threshold
        
        self._init_tts()
        print("[Voice] Initialized using sounddevice (PyAudio alternative).")

    def _init_tts(self):
        """Initialize text-to-speech engine."""
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", VOICE_SPEED)
            self.tts.setProperty("volume", VOICE_VOLUME)

            voices = self.tts.getProperty("voices")
            preferred = None
            for v in voices:
                name = v.name.lower()
                if "david" in name or "mark" in name or "george" in name:
                    preferred = v.id
                    break
            if not preferred and voices:
                preferred = voices[0].id
            if preferred:
                self.tts.setProperty("voice", preferred)
        except Exception as e:
            print(f"[TTS] Init error: {e}")

    def speak(self, text: str):
        """Speak text aloud in a thread-safe way."""
        if not self.tts: return
        self.is_speaking = True
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"[TTS] Error: {e}")
        finally:
            self.is_speaking = False

    def speak_async(self, text: str):
        """Speak without blocking the main thread."""
        t = threading.Thread(target=self.speak, args=(text,), daemon=True)
        t.start()

    def record_audio(self, duration=5):
        """Record audio from sounddevice and return as SR AudioData."""
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels, dtype='int16')
        sd.wait()
        
        # Convert to bytes
        byte_io = io.BytesIO()
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2) # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(recording.tobytes())
        
        byte_io.seek(0)
        with sr.AudioFile(byte_io) as source:
            return self.recognizer.record(source)

    def listen_once(self, timeout=8) -> str | None:
        """Capture audio and transcribe. Uses sounddevice for recording."""
        self.is_listening = True
        try:
            # We record a fixed window or use a more complex silence detection
            # For simplicity, we record 5 seconds
            audio = self.record_audio(duration=5)
            text = self.recognizer.recognize_google(audio)
            return text.lower().strip()
        except Exception:
            return None
        finally:
            self.is_listening = False

    def start_wake_word_loop(self):
        """Continuous background loop monitoring audio levels for the wake word."""
        self.active = True
        t = threading.Thread(target=self._wake_word_loop, daemon=True)
        t.start()
        print(f'[Wake] Always-listening for "{self.wake_word}"...')

    def _wake_word_loop(self):
        """Monitor sound levels. When sound is detected, capture and check for wake word."""
        # This is a robust implementation using sounddevice streaming
        def callback(indata, frames, time_info, status):
            if status: print(status)
            # Calculate volume
            volume_norm = np.linalg.norm(indata) * 10
            if volume_norm > 50 and not self.is_speaking and not self.is_listening:
                # Potential speech detected!
                # We need to handle this carefully to avoid recursion
                # In a thread, start a recording session
                threading.Thread(target=self._check_for_command).start()

        with sd.InputStream(callback=callback, channels=self.channels, samplerate=self.sample_rate):
            while self.active:
                time.sleep(0.1)

    def _check_for_command(self):
        if self.is_listening or self.is_speaking: return
        
        self.is_listening = True
        try:
            # Record 4 seconds to check for wake word or command
            audio = self.record_audio(duration=4)
            text = self.recognizer.recognize_google(audio).lower().strip()
            
            if self.wake_word in text:
                # Extract command after wake word
                idx = text.find(self.wake_word)
                command = text[idx + len(self.wake_word):].strip()
                
                if not command:
                    # User said just "Hey Friday", we should trigger a "Yes Sir?"
                    if self.on_command:
                        self.on_command("wake_only", source="voice")
                else:
                    if self.on_command:
                        self.on_command(command, source="voice")
        except Exception:
            pass
        finally:
            self.is_listening = False

    def stop(self):
        self.active = False
