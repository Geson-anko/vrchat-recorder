from typing import Any

import inputs

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
