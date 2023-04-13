# VRChat Recorder

VRChat Recorder is a tool for recording VRChat Videos, Audios, OSC Feedbacks, and Controller inputs.

## Installation

### Prerequaments

- Python 3.10+
- OBS Studio
  Enable Websocket Server in OBS Studio.
- VRChat
  Enable OSC.

### Install

Clone this repository and install it.

```bash
git clone "<URL>"
cd vrchat-recorder
pip install -e .
```

## Usage

```bash
python -m vrchat-recorder -d <directory>
```

このコマンドで記録を開始することができます。`Ctrl+C`で停止できます。
記録されたデータは`<directory>/<YYYY-MM-DD-hh-mm-ss-millisec>.vrcrec`ディレクトリに保存されます。通常はOBSの起動やVRChatのOSCの有効化を確認するためのメッセージが表示されます。

### Recording data

- プレイ動画・音声

  OBS Studioによって録画されます。事前にOBS Studioを起動し、VRChatの画面や音声が録画されるように設定しておいてください。

  録画はpythonによって自動的に開始され、記録された動画は`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.video.<ext>`に保存されます。このファイルはOBS Studioで設定された保存場所から移動されてるため、記録中に`.vrcrec`に動画ファイルは存在しません。
  ファイル名に含まれる時刻はディレクトリの時刻と少しずれます。また、`<ext>`はOBS Studioで設定されたファイル形式です。

- OSC フィードバックデータ

  VRChatによって送信されたOSCメッセージをCSV形式で記録します。デフォルトでは`avatar/parameters/`以下のメッセージのみ記録されます。
  ファイルは`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.oscfb.csv`に保存されます。ファイル名に含まれる時刻はディレクトリの時刻と少しだけずれる事があります。

  フォーマットは次のようなCSVです。

  ```csv
  timestamp,event_type,parameter_name,data_type,value
  1679657265.7147608,/avatar/parameters/AngularY,float,8.0
  ```

- ゲームパッドの入力データ

  ゲームパッドの入力データをCSV形式で記録します。
  ファイルは`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.<gamepad name>.gamepad.csv`に保存されます。ファイル名に含まれる時刻はディレクトリの時刻と少しだけずれる事があります。

  フォーマットは次のようなCSVです。

  ```csv
  timestamp,parameter_name,data_type,value
  1679657265.7147608,ABS_X,int,128
  ```

### Options

- `-d <directory>`, `--output-dir <directory>`:
  記録データを保存するディレクトリを指定します。デフォルトではカレントディレクトリです。

- `--no-ask`:
  記録開始時にOBSの起動やOSCの有効化を確認するかどうかを指定します。デフォルトでは確認します。

- `--date_format <format>`:
  ディレクトリ名に含まれる日付のフォーマットを指定します。デフォルトでは`%Y-%m-%d-%H-%M-%S-%f`です。

- `--log_level <level>`:
  ログレベルを指定します。デフォルトでは`INFO`です。

- `--vrchat_osc_ip <ip>`:
  VRChatのOSCを受信するIPアドレスを指定します。デフォルトでは`localhost`です。

- `--vrchat_osc_port <port>`:
  VRChatのOSCを受信するポート番号を指定します。デフォルトでは`9001`です。

- `--vrchat_osc_address <address>`:
  VRChatの受信するOSCアドレスを指定します。デフォルトでは`/avatar/parameters/*`です。

- `--obs_websocket_ip <ip>`:
  OBS StudioのWebsocketを受信するIPアドレスを指定します。デフォルトでは`localhost`です。

- `--obs_websocket_port <port>`:
  OBS StudioのWebsocketを受信するポート番号を指定します。デフォルトでは`4444`です。

- `--obs_websocket_password <password>`:
  OBS StudioのWebsocketのパスワードを指定します。WebSocketServerの認証設定をしていない場合は指定する必要はありません。

- `--mic_device_name <name>`, `--mic <name>`:
  録音するマイクのデバイス名を指定します。デフォルトではデフォルトのマイクを使用します。

- `mic_sample_rate <rate>`:
  録音するマイクのサンプリングレートを指定します。デフォルトでは`44100`です。

- `--mic_channels <channels>`:
  録音するマイクのチャンネル数を指定します。デフォルトでは`1`です。

- `--mic_block_size <size>`:
  録音するマイクのブロック(チャンク)サイズを指定します。デフォルトでは`4096`です。

- `--mic_flush_interval <interval>`:
  ファイルへ一度にフラッシュするブロックの数です。デフォルトでは`100`です。

- `--mic_subtype <subtype>`:
  録音する音声ファイルのサブタイプを指定します。デフォルトでは`PCM_16`です。

- `--speaker_device_name <name>`, `--speaker <name>`:
  録音するスピーカーのデバイス名を指定します。デフォルトではデフォルトのスピーカーを使用します。

- `--speaker_sample_rate <rate>`:
  録音するスピーカーのサンプリングレートを指定します。デフォルトでは`44100`です。

- `--speaker_channels <channels>`:
  録音するスピーカーのチャンネル数を指定します。デフォルトでは`2`です。

- `--speaker_block_size <size>`:
  録音するスピーカーのブロック(チャンク)サイズを指定します。デフォルトでは`4096`です

- `--speaker_flush_interval <interval>`:
  ファイルへ一度にフラッシュするブロックの数です。デフォルトでは`100`です。

- `--speaker_subtype <subtype>`:
  録音する音声ファイルのサブタイプを指定します。デフォルトでは`PCM_16`です。

- `--no_osc_feedback`:
  OSCフィードバックを記録しない場合は指定します。デフォルトでは記録します。

- `--no_gamepad`:
  ゲームパッドの入力を記録しない場合は指定します。デフォルトでは記録します。

- `--no_obs`:
  OBSを用いてプレイ映像および音声を録画しない場合は指定します。デフォルトでは記録します。

- `--no_mic`:
  マイクを用いて音声を録音しない場合は指定します。デフォルトでは記録します。

- `--no_speaker`:
  スピーカーを用いて音声を録音しない場合は指定します。デフォルトでは記録します。

## 開発途中

- [ ] マウスやヘッドセットの操作情報にも対応する。
  - [ ] マウスとキーボードによる操作記録機能の実装。
  - [ ] VRヘッドセットとコントローラによる操作記録機能の実装
- [ ] HMDに映っているいる映像も記録できるようにする。

## License

MIT.
