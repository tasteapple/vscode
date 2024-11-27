from flask import Flask, render_template_string
from scapy.all import sniff, IP, TCP
import threading

app = Flask(__name__)

# 캡처된 패킷의 정보를 저장할 리스트
captured_packets = []

# 패킷을 캡처하는 함수
def packet_callback(packet):
    if IP in packet:  # 패킷이 IP 계층을 포함하고 있는지 확인
        src_ip = packet[IP].src
        proto = packet[IP].proto
        protocol_name = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}.get(proto, 'Other')
        
        # HTTP 확인: TCP 패킷 중에서 포트 80으로의 통신인 경우 HTTP로 간주
        if TCP in packet and (packet[TCP].dport == 80 or packet[TCP].sport == 80):
            protocol_name = 'HTTP'
        
        packet_info = f"Source IP: {src_ip}, Protocol: {protocol_name}"
        captured_packets.append(packet_info)
        
        if len(captured_packets) > 50:  # 메모리 관리를 위해 최대 50개까지만 저장
            captured_packets.pop(0)

# 백그라운드에서 패킷을 캡처하는 스레드 시작
def start_packet_sniffing():
    sniff(prn=packet_callback, store=False)  # 모든 패킷을 캡처

# HTML 템플릿 정의
html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Packet Capture</title>
    <meta http-equiv="refresh" content="5"> <!-- 5초마다 자동 새로고침 -->
    <style>
        .packet {
            border: 1px solid #333;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
        }
    </style>
  </head>
  <body>
    <h1>Captured Packets</h1>
    <div>
      {% for packet in packets %}
        <div class="packet">
            <pre>{{ packet }}</pre>
        </div>
      {% endfor %}
    </div>
  </body>
</html>
"""

# Flask 라우트 정의
@app.route('/')
def index():
    return render_template_string(html_template, packets=captured_packets)

# 메인 함수
if __name__ == '__main__':
    # 패킷 캡처를 위한 스레드 시작
    sniffing_thread = threading.Thread(target=start_packet_sniffing, daemon=True)
    sniffing_thread.start()

    # Flask 서버 시작
    app.run(host='0.0.0.0', port=4000)
