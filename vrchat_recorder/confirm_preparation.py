from typing import Any

import inputs
import soundcard as sc

confirm_about_obs_prompt = """\
確認: OBS
1. OBSはインストールされ、起動していますか？
2. OBSはVRChatのゲーム画面をキャプチャしていますか？
3. OBSは音声を記録していますか？
4. OBSのWebSocketサーバは有効化されていますか？
5. WebSocketのサーバIP:PORTは `{0}:{1}` ですか？また、パスワードは正しいですか？
"""


confirm_about_vrchat_prompt = """\
確認: VRChat
1. VRChatはインストールされ、起動していますか？
2. VRChatはデスクトップモードで起動していますか？
3. VRChat OSC機能は有効化されていますか？
4. VRChatのOSCの受信をするためのサーバIP:PORTは `{0}:{1}` ですか？
5. OSCのAddressは `{2}` で正しいですか？
"""

confirm_about_controller_prompt = """\
確認: コントローラ
1. Gamepadは接続されていますか？
2. 現在表示しているデバイス一覧にあなたのGamepadは表示されていますか？
デバイス一覧:
{0}
"""

confirm_about_mic_prompt = """\
確認: マイク
選択されたマイクのデバイス名は `{0}` で正しいですか？
サンプリングレートは `{1}` で正しいですか？
チャネル数は `{2}` で正しいですか？
正しくない場合は次のデバイスリストから正しい名前を指定してください。
{3}
"""

confirm_about_speaker_prompt = """\
確認: スピーカー
選択されたスピーカーのデバイス名は `{0}` で正しいですか？
サンプリングレートは `{1}` で正しいですか？
チャネル数は `{2}` で正しいですか？
正しくない場合は次のデバイスリストから正しい名前を指定してください。
スピーカーはループバックデバイスとして録音されます。
{3}
"""

confirm_about_vr_recording_prompt = """\
確認: VR デバイスの記録
1. VRモードでVRChatを起動していますか？
2. ヘッドセットやコントローラーは接続されていますか？
3. トラッキングデータを取得するFPSは `{0}` で正しいですか？
"""


def confirm_about_obs(OBS_WEBSOCKET_IP: Any, OBS_WEBSOCKET_PORT: int) -> None:
    """Confirm about OBS.

    Args:
        OBS_WEBSOCKET_IP (Any): OBS WebSocket server IP.
        OBS_WEBSOCKET_PORT (int): OBS WebSocket server port.
    """
    print(confirm_about_obs_prompt.format(OBS_WEBSOCKET_IP, OBS_WEBSOCKET_PORT), end="")
    input()


def confirm_about_vrchat(VRCHAT_OSC_IP: Any, VRCHAT_OSC_PORT: int, OSC_ADDRESS: str) -> None:
    """Confirm about VRChat.

    Args:
        VRCHAT_OSC_IP (Any): VRChat OSC server IP.
        VRCHAT_OSC_PORT (int): VRChat OSC server port.
        OSC_ADDRESS (str): OSC address.
    """
    print(confirm_about_vrchat_prompt.format(VRCHAT_OSC_IP, VRCHAT_OSC_PORT, OSC_ADDRESS), end="")
    input()


def confirm_about_controller() -> None:
    """Confirm about controller."""
    controller_names = "\n".join([f"{i}: {controller.name}" for i, controller in enumerate(inputs.devices.gamepads)])
    print(confirm_about_controller_prompt.format(controller_names), end="")
    input()


def confirm_about_mic(mic_name: str, mic_sampling_rate: int, mic_channels: int) -> None:
    """Confirm about microphone.

    Args:
        mic_name (str): Microphone name.
        mic_sampling_rate (int): Microphone sampling rate.
        mic_channels (int): Microphone channels.
    """
    mic_names = "\n".join([f"{i}: {mic.name}" for i, mic in enumerate(sc.all_microphones())])
    print(confirm_about_mic_prompt.format(mic_name, mic_sampling_rate, mic_channels, mic_names), end="")
    input()


def confirm_about_speaker(speaker_name: str, speaker_sampling_rate: int, speaker_channels: int) -> None:
    """Confirm about speaker.

    Args:
        speaker_name (str): Speaker name.
        speaker_sampling_rate (int): Speaker sampling rate.
        speaker_channels (int): Speaker channels.
    """
    speaker_names = "\n".join(
        [f"{i}: {speaker.name}" for i, speaker in enumerate(sc.all_microphones(include_loopback=True))]
    )
    print(
        confirm_about_speaker_prompt.format(speaker_name, speaker_sampling_rate, speaker_channels, speaker_names),
        end="",
    )
    input()


def confirm_about_vr_recording(fps: float) -> None:
    """Confirm about VR recording.

    Args:
        fps (float): FPS.
    """
    print(confirm_about_vr_recording_prompt.format(fps), end="")
    input()
