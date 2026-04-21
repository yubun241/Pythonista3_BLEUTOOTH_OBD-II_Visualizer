## Pythonista3_BLUETOOTH_OBD-II_Visualizer
Pythonista 3（iOS）を使用して、BMW/MINIの車両情報をBluetooth Low Energy (BLE) 経由で取得し、リアルタイムに可視化するためのツールです。

## 概要 (Description)
このプロジェクトは、iPhoneやiPad上のPythonista 3環境で、

ELM327互換のBLE OBD-IIアダプタと通信し、車両の各種センサーデータをデジタル表示するものです。

特にMINI JCW (F56 前期型) での動作をターゲットとしています。

## 主な機能 (Features)
リアルタイム・モニタリング: 以下の項目をデジタル表示します。

Engine RPM: エンジン回転数

Water Temperature: エンジン冷却水温

Oil Temperature: エンジンオイル温度

Boost Pressure: ブースト圧（マニホールド絶対圧からの計算値）

Current Gear: 現在のギア段数（車速と回転数からの計算、または専用PID）

BLE通信: iOSの cb モジュールを利用した低消費電力通信。

独自UI: Pythonistaの ui モジュールによるカスタマイズ可能なダッシュボード。


## 動作環境 (Requirements)
Hardware:

iOSデバイス（iPhone / iPad）

BLE (Bluetooth Low Energy) 対応のOBD-IIアダプタ（例: vLinker MC+, LELink, などのELM327互換機）

BMW MINI JCW (F56) または同世代のBMW/MINI車両

Software:

Pythonista 3 (iOS App)


## 使用方法 (How to Use)
OBD-IIアダプタを車両のOBDポートに接続し、イグニッションをON（またはエンジン始動）にします。

obd_monitor.py をPythonista 3にダウンロードまたはコピーします。

スクリプトを実行すると、周辺のBLEデバイスのスキャンが開始されます。

対象のアダプタが発見されると自動的に接続され、データの取得と表示が始まります。


## 技術詳細 (Technical Details)
取得PIDと計算ロジック

項目	Mode/PID	計算式

水温	01 05	$A - 40$

エンジン回転数	01 0C	$((A \times 256) + B) / 4$

油温	01 5C	$A - 40$

ブースト圧	01 0B	$A - 101.3$ (kPa)


## 通信プロトコル
ELM327 AT Commands: 初期化時に ATZ, ATE0, ATL0 等を送信し、通信を最適化しています。

Event-Driven: Pythonistaの CentralManagerDelegate を活用した非同期通信を採用。

免責事項 (Disclaimer)
本ツールは個人の趣味の範囲で開発されたものです。運転中の操作は避け、安全な場所で使用してください。本ツールを使用したことによる車両の不具合や事故等について、開発者は一切の責任を負いません。
