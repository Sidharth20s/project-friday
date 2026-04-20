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
        self.sample_rate = 16000  # Google Speech API prefers 16kHz
        self.channels = 1
        self.energy_threshold = 300 # Default SR threshold
        
        self._init_tts()
        print("[Voice] Initialized using sounddevice (PyAudio alternative).")

    def _init_tts(self):
        """Initialize text-to-speech engine with female voice."""
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", VOICE_SPEED)
            self.tts.setProperty("volume", VOICE_VOLUME)

            voices = self.tts.getProperty("voices")
            preferred = None
            
            # Prefer female voices: Zira, Victoria, Cortana, etc.
            for v in voices:
                name = v.name.lower()
                if "zira" in name or "victoria" in name or "cortana" in name or "samantha" in name:
                    preferred = v.id
                    break
            
            # If no female voice found, pick any available voice
            if not preferred and voices:
                # Try to find female voice by checking gender
                for v in voices:
                    try:
                        if hasattr(v, 'gender') and 'female' in str(v.gender).lower():
                            preferred = v.id
                            break
                    except:
                        pass
                
                # Fall back to first voice if still nothing found
                if not preferred:
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
        import warnings
        warnings.filterwarnings('ignore')  # Suppress sounddevice warnings
        
        try:
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
        except Exception as e:
            print(f"[Audio] Recording error: {e}")
            return None

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
        """Continuously listen for wake word using Google Speech Recognition."""
        import warnings
        warnings.filterwarnings('ignore')
        
        print(f'[Wake] Listening continuously for "{self.wake_word}"...')
        
        while self.active:
            try:
                if self.is_speaking or self.is_listening:
                    time.sleep(0.5)
                    continue
                
                # Always recording 3-second chunks to check for wake word
                print("[Wake] Recording 3 seconds for wake word detection...")
                audio = self.record_audio(duration=3)
                
                try:
                    # Transcribe the audio
                    text = self.recognizer.recognize_google(audio).lower().strip()
                    print(f"[Wake] Heard: {text}")
                    
                    # Check if wake word is in the text
                    if self.wake_word in text:
                        print(f"[Wake] ✓ WAKE WORD DETECTED: '{self.wake_word}'")
                        
                        # Extract command after wake word
                        idx = text.find(self.wake_word)
                        command = text[idx + len(self.wake_word):].strip()
                        
                        if command:
                            # User already said command with wake word
                            print(f"[Wake] Executing command: {command}")
                            if self.on_command:
                                self.on_command(command, source="voice")
                        else:
                            # Only wake word, listen for next command
                            print("[Wake] Waiting for command...")
                            time.sleep(0.5)
                            self._listen_for_command()
                            
                except sr.UnknownValueError:
                    # Audio not understood, continue listening
                    pass
                except sr.RequestError as e:
                    print(f"[Wake] Speech API error: {e}")
                    time.sleep(2)  # Wait before retrying
                    
            except Exception as e:
                print(f"[Wake] Error: {e}")
                time.sleep(1)

    def _listen_for_command(self):
        """After wake word detected, listen for the actual command."""
        if self.is_listening or self.is_speaking:
            return
        
        self.is_listening = True
        try:
            print("[Listen] Recording command (5 seconds)...")
            audio = self.record_audio(duration=5)
            
            if audio is None:
                print("[Listen] No audio recorded")
                return
            
            text = self.recognizer.recognize_google(audio).lower().strip()
            
            if text:
                print(f"[Listen] Command: {text}")
                if self.on_command:
                    self.on_command(text, source="voice")
        except sr.UnknownValueError:
            print("[Listen] Could not understand audio")
        except sr.RequestError as e:
            print(f"[Listen] Speech API error: {e}")
        finally:
            self.is_listening = False

    def stop(self):
        self.active = False
