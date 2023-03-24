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

このコマンドは記録を開始します。`Ctrl+C`で停止できます。
記録されたデータは`<directory>/<YYYY-MM-DD-hh-mm-ss-millisec>.vrcrec`ディレクトリに保存されます。

### Recording data

- プレイ動画・音声
  OBS Studioによって録画されます。事前にOBS Studioを起動し、VRChatの画面や音声が録画されるように設定しておいてください。
  録画はpythonによって自動的に開始され、記録された動画は`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.video.<ext>`に保存されます。このファイルはOBS Studioで設定された保存場所から移動されてるため、記録中に`.vrcrec`に動画ファイルは存在しません。
  ファイル名に含まれる時刻はディレクトリの時刻と一致します。また、`<ext>`はOBS Studioで設定されたファイル形式です。

- OSC フィードバックデータ
  VRChatによって送信されたOSCメッセージをCSV形式で記録します。デフォルトでは`avatar/parameters/`以下のメッセージのみ記録されます。
  ファイルは`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.oscfeedback.csv`に保存されます。ファイル名に含まれる時刻はディレクトリの時刻と少しだけずれる事があります。

  フォーマットは次のようなCSVです。

  ```csv
  timestamp,parameter_name,data_type,value
  1679657265.7147608,/avatar/parameters/AngularY,float,8.0
  ```

- コントローラ入力データ
  コントローラの入力データをCSV形式で記録します。
  ファイルは`.vrcrec/<YYYY-MM-DD-hh-mm-ss-millisec>.<controller_name>.controller.csv`に保存されます。ファイル名に含まれる時刻はディレクトリの時刻と少しだけずれる事があります。

  フォーマットは次のようなCSVです。

  ```csv
  timestamp,input_name,data_type,value
  1679657265.7147608,ABS_X,int,128
  ```

### Options

## Development

- [ ] マウスやヘッドセットの操作情報にも対応する。
  - [ ] マウスとキーボードによる操作記録機能の実装。
  - [ ] VRヘッドセットとコントローラによる操作記録機能の実装
- [ ] HMDに映っているいる映像も記録できるようにする。

## License

MIT.
