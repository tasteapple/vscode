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
        
        packet_info = {
            "input_id": len(captured_packets) + 1,
            "input_passwd": "N/A",  # 패킷 캡처에서는 비밀번호 정보가 없으므로 N/A로 설정
            "source_addr": src_ip,
            "result": protocol_name,
            "time": packet.time
        }
        captured_packets.append(packet_info)
        
        if len(captured_packets) > 50:  # 메모리 관리를 위해 최대 50개까지만 저장
            captured_packets.pop(0)

# 백그라운드에서 패킷을 캡처하는 스레드 시작
def start_packet_sniffing():
    sniff(prn=packet_callback, store=False)  # 모든 패킷을 캡처

# HTML 템플릿 정의 (dashboard.html의 내용 포함)
dashboard_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
      * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
      }

      body {
          font-family: Arial, sans-serif;
          background-color: #f5f5f5;
      }

      /* Dashboard Page Styles */
      .dashboard {
          padding: 2rem;
      }

      .dashboard-title {
          margin-bottom: 2rem;
          color: #333;
      }

      .log-table {
          width: 100%;
          background: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      .log-table table {
          width: 100%;
          border-collapse: collapse;
      }

      .log-table th,
      .log-table td {
          padding: 1rem;
          text-align: left;
          border-bottom: 1px solid #eee;
      }

      .log-table th {
          background-color: #f8f8f8;
          font-weight: bold;
          color: #666;
      }
      .log-table tr{
        border-bottom: #666 solid 1px;
      }

      .attack-log {
        background: rgba(234, 81, 30, 0.3);
      }
  </style>
</head>
<body>
  <div class="dashboard">
    <h1 class="dashboard-title">LOG</h1>
    <div class="log-table">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>PW</th>
                    <th>IP</th>
                    <th>RESULT</th>
                    <th>TIME</th>
                </tr>
            </thead>
            <tbody id="logTable">
              {% for log in packets %}
                <tr class="{% if log.result == 'HTTP' %}attack-log{% endif %}">
                    <td>{{ log.input_id }}</td>
                    <td>{{ log.input_passwd }}</td>
                    <td>{{ log.source_addr }}</td>
                    <td>{{ log.result }}</td>
                    <td>{{ log.time }}</td>
                </tr>
              {% endfor %}
            </tbody>
        </table>
    </div>
  </div>
</body>
</html>
"""

# Flask 라우트 정의
@app.route('/')
def index():
    return render_template_string(dashboard_template, packets=captured_packets)

# 메인 함수
if __name__ == '__main__':
    # 패킷 캡처를 위한 스레드 시작
    sniffing_thread = threading.Thread(target=start_packet_sniffing, daemon=True)
    sniffing_thread.start()

    # Flask 서버 시작
    app.run(host='0.0.0.0', port=4000)
