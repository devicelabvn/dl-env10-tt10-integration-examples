# DL-ENV10 Environmental Datalogger - Thông Tư 10/2021/TT-BTNMT & Nghị Định 53/2024 Integration Examples 🌿

> **Tài liệu tích hợp mở, mẫu tệp tin `.txt` truyền dẫn FTPS, cấu trúc gói tin MQTT JSON, REST API và Bảng thanh ghi Modbus TCP của thiết bị Datalogger quan trắc môi trường tự động `DL-ENV10`.**  
> Phát triển và sản xuất bởi **[DeviceLab](https://devicelab.vn/)** (CÔNG TY TNHH ĐẦU TƯ CÔNG NGHỆ ALPHA TECH - MST: `0111171963`).  
> 🔗 **Trang thông số sản phẩm:** [Datalogger Quan Trắc Môi Trường TT10 DL-ENV10](https://devicelab.vn/san-pham/dl-env10/) ([English Version](https://devicelab.vn/en/products/dl-env10/))  
> 🔗 **Giải pháp cho Nhà thầu SI Môi trường:** [Datalogger Quan Trắc Môi Trường Chuẩn Thông Tư 10](https://devicelab.vn/datalogger-quan-trac-moi-truong-tt10/)  
> 📖 **Đọc bài phân tích chi tiết tiếng Việt trên Viblo & Tinh Tế:**  
> - **Trên Viblo.asia:** [Kinh nghiệm xử lý mất dữ liệu trạm quan trắc & Quy chuẩn phần cứng Datalogger theo Điều 39 Thông tư 10/2021/TT-BTNMT](https://viblo.asia/p/kinh-nghiem-xu-ly-mat-du-lieu-tram-quan-trac-quy-chuan-phan-cung-datalogger-theo-dieu-39-thong-tu-102021tt-btnmt-kNLr3eobVgA)  
> - **Trên Tinh Tế (`tinhte.vn`):** [Kinh nghiệm xử lý mất dữ liệu trạm quan trắc & chuẩn phần cứng Datalogger Thông tư 10](https://tinhte.vn/thread/kinh-nghiem-xu-ly-mat-du-lieu-tram-quan-trac-chuan-phan-cung-datalogger-thong-tu-10.4185068/)  
> - **Trên Dev.to (English):** [Why Windows IPCs Fail in Harsh Telemetry Stations & How RTOS Dataloggers Solve It](https://dev.to/thaodmtt/why-windows-ipcs-fail-in-harsh-telemetry-stations-how-rtos-embedded-dataloggers-solve-it-41ma)

---

## 📌 Tổng Quan Quy Chuẩn Kỹ Thuật (Điều 39 Thông Tư 10/2021/TT-BTNMT)

Thiết bị **[Datalogger quan trắc môi trường DL-ENV10](https://devicelab.vn/san-pham/dl-env10/)** được thiết kế chuyên dụng cho các trạm quan trắc nước thải, khí thải công nghiệp tự động liên tục và trạm quan trắc khai thác nước ngầm, nước mặt, hồ thủy điện (theo **Nghị định 53/2024/NĐ-CP** & **Thông tư 17/2021/TT-BTNMT**):

| Hạng mục kỹ thuật | Yêu cầu tại Điều 39 TT10/2021/TT-BTNMT | Thông số đáp ứng trên `DeviceLab DL-ENV10` |
| :--- | :--- | :--- |
| **Ngõ vào tín hiệu đo** | Thu nhận đồng thời tín hiệu Analog & Digital từ các đầu đo | **4x AI (`4–20mA` / `0–10V`, ADC 16-bit cách ly)**, **4x DI (đếm xung 10kHz)**, **1x RS485 Modbus RTU cách ly 2.5kV** (mở rộng tối đa 3 module I/O: `AI-8`, `RTD/TC-4`, `DI-8`, `DO-4`, `COM-2`, `Energy 3P`) |
| **Định dạng & Chu kỳ truyền** | Tệp `.txt` mã hóa UTF-8, chu kỳ truyền tối đa 5 phút/lần qua FTP/FTPS | Tự động xuất file `[MãTrạm]_[YYYYMMDDHHMMSS].txt` chuẩn UTF-8, đẩy qua **FTPS / SFTP** chu kỳ **5 phút/lần** về máy chủ Sở TN&MT 63 tỉnh thành |
| **Mã trạng thái thiết bị** | Ghi nhận đầy đủ trạng thái đo bình thường, hiệu chuẩn, báo lỗi | Tự động gán mã trạng thái cho từng thông số: `00` (Bình thường), `01` (Đang hiệu chuẩn - Calibration), `02` (Lỗi thiết bị đo - Sensor Error) |
| **Lưu đệm & Truyền bù** | Lưu trữ dữ liệu tối thiểu 60 ngày, tự động truyền bù khi có mạng | Bộ nhớ Flash công nghiệp lưu **100.000 bản ghi** + khe cắm thẻ nhớ lưu **> 180 ngày**; cơ chế **Store & Forward** tự động đẩy bù các file `.txt` bị thiếu ngay khi khôi phục mạng 4G/LAN |
| **Điều khiển lấy mẫu tự động** | Kích hoạt máy lấy mẫu khi thông số vượt ngưỡng quy chuẩn | **2x DO Relay (250VAC/5A)** điều khiển trực tiếp tủ lấy mẫu tự động (**Auto Sampler**) bảo quản mẫu nước đối chứng khi `COD`, `TSS`, `pH`, `Amoni` vượt ngưỡng QCVN |

---

## 1. Cấu Trúc File `.txt` Chuẩn Thông Tư 10/2021/TT-BTNMT (Trạm Nước Thải & Khí Thải)

Tên file được tự động sinh theo định dạng: `[TenTinh]_[TenCongTy]_[MaTram]_[YYYYMMDDHHMMSS].txt`, các trường dữ liệu phân tách bằng ký tự `Tab` (`\t`), mã hóa `UTF-8`:

```text
pH	7.42	pH	20261015103000	00
COD	48.50	mg/L	20261015103000	00
TSS	28.10	mg/L	20261015103000	00
NH4	3.82	mg/L	20261015103000	00
Temp	29.60	oC	20261015103000	00
Flow_In	148.20	m3/h	20261015103000	00
Flow_Out	142.80	m3/h	20261015103000	00
```

> 📂 Xem file mẫu đầy đủ tại: [`samples/KCN_TAMDIEP_NT_20261015103000.txt`](./samples/KCN_TAMDIEP_NT_20261015103000.txt)

---

## 2. Cấu Trúc File `.txt` Quan Trắc Nước Ngầm & Nước Mặt (Nghị Định 53/2024/NĐ-CP & TT 17)

Dành cho trạm quan trắc giếng khoan khai thác nước dưới đất và trạm thủy điện truyền dữ liệu về Cục Quản lý Tài nguyên nước / Sở TN&MT:

```text
LuuLuongTucThoi	45.20	m3/h	20261015080000	00
LuuLuongTichLuy	128450.50	m3	20261015080000	00
MucNuocDong	-28.45	m	20261015080000	00
MucNuocTinh	-14.20	m	20261015080000	00
```

> 📂 Xem file mẫu đầy đủ tại: [`samples/ND_CONGTYABC_GIENG01_20261015080000.txt`](./samples/ND_CONGTYABC_GIENG01_20261015080000.txt)

---

## 3. Cấu Trúc Bản Tin JSON Qua MQTT (Dành Cho Phần Mềm Giám Sát & Cloud)

Bên cạnh luồng FTPS đẩy về Sở TN&MT, `DL-ENV10` hỗ trợ xuất đồng thời dữ liệu thời gian thực qua **MQTT / MQTTS (TLS 1.2/1.3)** về máy chủ nội bộ của nhà máy hoặc ứng dụng di động:

- **MQTT Topic mặc định:** `devicelab/DL-ENV10-01/telemetry`

```json
{
  "device_id": "DL-ENV10-01",
  "station_code": "KCN_TAMDIEP_NT",
  "ts": "2026-10-15T10:30:00+07:00",
  "net": {
    "type": "4g_lte",
    "rssi": -68,
    "ftp_queue_pending": 0
  },
  "points": [
    { "id": "ph", "name": "Do_pH", "val": 7.42, "unit": "pH", "status": "00" },
    { "id": "cod", "name": "Chi_so_COD", "val": 48.5, "unit": "mg/L", "status": "00" },
    { "id": "tss", "name": "Chat_ran_TSS", "val": 28.1, "unit": "mg/L", "status": "00" },
    { "id": "nh4", "name": "Amoni_NH4", "val": 3.82, "unit": "mg/L", "status": "00" },
    { "id": "temp", "name": "Nhiet_do", "val": 29.6, "unit": "oC", "status": "00" },
    { "id": "flow", "name": "Luu_luong_ra", "val": 142.8, "unit": "m3/h", "status": "00" }
  ],
  "io_state": {
    "door_open": false,
    "grid_power_ok": true,
    "autosampler_triggered": false
  }
}
```

---

## 4. Bảng Thanh Ghi Modbus TCP Server & Local REST API (Cho SCADA / PLC Tại Trạm)

`DL-ENV10` tích hợp sẵn **Modbus TCP Server (Port `502`, Unit ID `1`)** và **HTTP REST API** giúp hệ thống SCADA/HMI tại phòng điều khiển trung tâm đọc số liệu trực tiếp mà không ảnh hưởng đến luồng truyền FTPS:

### A. Bảng Thanh Ghi Modbus TCP (`Float32 Big-Endian` - 2 Thanh ghi / Điểm đo)

| Địa chỉ Thanh ghi | Mã Tín hiệu | Mô tả thông số | Kiểu dữ liệu | Đơn vị | Quyền truy cập |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`30001` – `30002`** | `ai1` | Độ pH nước thải đầu ra | `Float32 (ABCD)` | `pH` | Read Only (`FC 04`) |
| **`30003` – `30004`** | `ai2` | Chỉ số nhu cầu oxy hóa học COD | `Float32 (ABCD)` | `mg/L` | Read Only (`FC 04`) |
| **`30005` – `30006`** | `ai3` | Tổng chất rắn lơ lửng TSS | `Float32 (ABCD)` | `mg/L` | Read Only (`FC 04`) |
| **`30007` – `30008`** | `ai4` | Chỉ số Amoni ($\text{NH}_4^+\text{-N}$) | `Float32 (ABCD)` | `mg/L` | Read Only (`FC 04`) |
| **`30009` – `30010`** | `ai5_temp` | Nhiệt độ nước thải đầu ra | `Float32 (ABCD)` | `°C` | Read Only (`FC 04`) |
| **`30101` – `30102`** | `mb_flow` | Lưu lượng nước thải kênh hở (RS485) | `Float32 (ABCD)` | `m3/h` | Read Only (`FC 04`) |
| **`00001` (Coil)** | `do1_sample` | Kích hoạt máy lấy mẫu tự động | `Boolean` | `1 = Pulse` | Read / Write (`FC 01/05`) |
| **`00002` (Coil)** | `do2_alarm` | Bật/tắt còi đèn cảnh báo vượt ngưỡng | `Boolean` | `1 = ON` | Read / Write (`FC 01/05`) |

### B. Truy vấn nhanh qua Local HTTP REST API

```bash
$ curl -s http://192.168.1.100/api/v1/points | jq .
[
  { "id": "ai1", "name": "pH", "value": 7.42, "unit": "pH", "quality": "good", "tt10_status": "00" },
  { "id": "ai2", "name": "COD", "value": 48.5, "unit": "mg/L", "quality": "good", "tt10_status": "00" },
  { "id": "mb1", "name": "LuuLuong", "value": 142.8, "unit": "m3/h", "quality": "good", "tt10_status": "00" }
]
```

---

## 5. Sơ Đồ Chân Đấu Nối Domino 22-Pin (`DL-ENV10` Base Unit)

- **Cầu đấu phía trên (Top Rail - 12 chân):**
  - `V+`, `V-`, `PE`: Ngõ vào nguồn chính `9–36VDC` (chống ngược cực, chống xung sét TVS) & Tiếp địa vỏ tủ.
  - `24V`, `0V`: Ngõ ra nguồn phụ cấp nuôi cảm biến 2 dây `4–20mA` (Loop-powered).
  - `A`, `B`, `G`: Cổng **RS485 Modbus RTU cách ly quang 2.5kV** kết nối tủ phân tích đa chỉ tiêu (Hach SC200/SC1000, Endress+Hauser Liquiline CM44x, WTW, Horiba...).
  - `NO1`, `C1` & `NO2`, `C2`: 2 cặp tiếp điểm rơ-le khô điều khiển máy lấy mẫu tự động và còi báo động.
- **Cầu đấu phía dưới (Bottom Rail - 10 chân):**
  - `AI1`, `AI2`, `AI3`, `AI4`, `AG`: 4 kênh Analog Input `4–20mA` / `0–10V` độ phân giải 16-bit và chân Mass Analog chung (`AG`).
  - `DI1`, `DI2`, `DI3`, `DI4`, `DG`: 4 kênh Digital Input cách ly quang (nhận báo trạng thái cửa tủ, trạng thái hiệu chuẩn `Calib_Active` từ máy phân tích để tự động chuyển mã trạng thái từ `00` sang `01`).

---

## 📖 Tài Liệu Chuyên Sâu Về Datalogger Quan Trắc Môi Trường (DeviceLab Knowledge Hub)

- [Cẩm nang Datalogger quan trắc môi trường Thông tư 10/2021/TT-BTNMT toàn tập](https://devicelab.vn/kien-thuc/cam-nang-datalogger-quan-trac-moi-truong-tt10/)
- [Quy chuẩn kỹ thuật Datalogger theo Điều 39 Thông tư 10/2021/TT-BTNMT](https://devicelab.vn/kien-thuc/quy-chuan-datalogger-dieu-39-thong-tu-10-2021-tt-btnmt/)
- [So sánh Máy tính công nghiệp (IPC) và Datalogger nhúng RTOS trong trạm quan trắc](https://devicelab.vn/kien-thuc/so-sanh-may-tinh-cong-nghiep-ipc-va-datalogger-nhung/)
- [Cơ chế lưu đệm Flash và truyền bù dữ liệu (Store & Forward) khi mất mạng](https://devicelab.vn/kien-thuc/co-che-luu-dem-flash-truyen-bu-du-lieu-datalogger/)
- [Datalogger quan trắc khai thác nước ngầm, nước mặt tự động theo Nghị định 53/2024](https://devicelab.vn/kien-thuc/datalogger-quan-trac-khai-thac-nuoc-ngam-nuoc-mat-tu-dong/)

### 🌐 Đọc bài phân tích chi tiết tiếng Việt trên Viblo & Tinh Tế:
- **[Viblo.asia]** [Kinh nghiệm xử lý mất dữ liệu trạm quan trắc & Quy chuẩn phần cứng Datalogger theo Điều 39 Thông tư 10/2021/TT-BTNMT](https://viblo.asia/p/kinh-nghiem-xu-ly-mat-du-lieu-tram-quan-trac-quy-chuan-phan-cung-datalogger-theo-dieu-39-thong-tu-102021tt-btnmt-kNLr3eobVgA)
- **[Tinh Tế (`tinhte.vn`)]** [Kinh nghiệm xử lý mất dữ liệu trạm quan trắc & chuẩn phần cứng Datalogger Thông tư 10](https://tinhte.vn/thread/kinh-nghiem-xu-ly-mat-du-lieu-tram-quan-trac-chuan-phan-cung-datalogger-thong-tu-10.4185068/)
- **[Viblo.asia]** [Từ bo mạch mẫu (Prototype) đến sản xuất 1.000 thiết bị IoT công nghiệp: Checklist thiết kế PCB chuẩn DFM & chống nhiễu EMC](https://viblo.asia/p/tu-bo-mach-mau-prototype-den-san-xuat-1000-thiet-bi-iot-cong-nghiep-checklist-thiet-ke-pcb-chuan-dfm-chong-nhieu-emc-OXLA0WqvJGr)
- **[Tinh Tế (`tinhte.vn`)]** [Từ bo mạch mẫu (Prototype) đến sản xuất 1.000 thiết bị IoT: Checklist thiết kế PCB & EMC](https://tinhte.vn/thread/tu-bo-mach-mau-prototype-den-san-xuat-1-000-thiet-bi-iot-checklist-thiet-ke-pcb-emc.4185069/)
- **[Viblo.asia]** [Phân biệt Transparent Converter và Modbus Gateway: Cách xử lý nhiễu biến tần và lưu đệm Flash khi rớt mạng 4G](https://viblo.asia/p/phan-biet-transparent-converter-va-modbus-gateway-cach-xu-ly-nhieu-bien-tan-va-luu-dem-flash-khi-rot-mang-4g-bA46807wLKv)
- **[Dev.to (EN)]** [Why Windows IPCs Fail in Harsh Telemetry Stations & How RTOS Dataloggers Solve It](https://dev.to/thaodmtt/why-windows-ipcs-fail-in-harsh-telemetry-stations-how-rtos-embedded-dataloggers-solve-it-41ma)

---

## 📞 Liên Hệ Tư Vấn Kỹ Thuật & Nhận Báo Giá Dự Án

- **Đơn vị sản xuất:** CÔNG TY TNHH ĐẦU TƯ CÔNG NGHỆ ALPHA TECH (**[DeviceLab](https://devicelab.vn/)**) - MST: `0111171963`
- **Địa chỉ R&D Lab:** Số 32/4, Hà Trì 4, Phường Hà Đông, TP. Hà Nội, Việt Nam
- **Hotline / Zalo Kỹ sư trưởng ([Đinh Mạnh Thảo](https://devicelab.vn/tac-gia/dinh-manh-thao/)):** `0982 503 355`
- **Email:** `contact@devicelab.vn` | `hi@devicelab.vn`
- **Yêu cầu báo giá dự án SI / OEM:** [https://devicelab.vn/san-pham/dl-env10/#bao-gia-du-an](https://devicelab.vn/san-pham/dl-env10/#bao-gia-du-an)


---

## Industrial IoT Hardware, Telemetry & Custom R&D Reference Index (DeviceLab Vietnam)

Official open engineering reference hubs, hardware datasheets, and compliance application notes maintained by **DeviceLab R&D Center** (Hanoi, Vietnam):

### 1. Industrial RS485, Modbus RTU/TCP & Edge Gateways
- [Bộ chuyển đổi RS485 sang Ethernet công nghiệp (Cách ly 3.0kV & Modbus RTU/TCP)](https://devicelab.vn/kien-thuc/bo-chuyen-doi-rs485-sang-ethernet/)
- [Thiết bị chuyển đổi tín hiệu RS485 cách ly DL-RS485 (Datasheet & Sơ đồ đấu nối)](https://devicelab.vn/san-pham/dl-rs485/)
- [Cẩm nang chọn Gateway Modbus RS485 sang Ethernet/4G LTE công nghiệp](https://devicelab.vn/kien-thuc/gateway-modbus-rs485/)
- [Bộ chuyển đổi Modbus RTU sang Modbus TCP: Kiến trúc Polling & Multi-Master](https://devicelab.vn/kien-thuc/bo-chuyen-doi-modbus-rtu-sang-tcp/)
- [Tiêu chuẩn cáp tín hiệu RS485 chống nhiễu 120 Ohm (22AWG/24AWG STP)](https://devicelab.vn/kien-thuc/cap-tin-hieu-rs485-chong-nhieu-tieu-chuan-chon/)
- [Đối chiếu thay thế Moxa MGate MB3180, Advantech EKI-1221, USR & 3onedata](https://devicelab.vn/kien-thuc/so-sanh-thay-the-modbus-gateway-moxa-mgate-advantech-usr-3onedata/)
- [Bộ chuyển đổi 4-20mA Analog sang RS485 Modbus & Module Remote I/O](https://devicelab.vn/kien-thuc/bo-chuyen-doi-4-20ma-analog-sang-rs485-remote-io-modbus/)
- [Industrial RS485 to Ethernet Converter Selection Guide (English)](https://devicelab.vn/en/articles/rs485-to-ethernet-converter-selection-guide/)

### 2. Circular 10/2021/TT-BTNMT Environmental Telemetry & SCADA RTU
- [Giải pháp Datalogger quan trắc môi trường tự động chuẩn Thông tư 10/2021/TT-BTNMT](https://devicelab.vn/datalogger-quan-trac-moi-truong-tt10/)
- [Kiến trúc trạm quan trắc nước thải tự động, liên tục & kết nối FTP Sở TN&MT](https://devicelab.vn/kien-thuc/datalogger-quan-trac-nuoc-thai-tu-dong/)
- [Thiết bị Datalogger quan trắc môi trường DL-ENV10 (Datasheet PDF)](https://devicelab.vn/san-pham/dl-env10/)
- [Quy chuẩn nước thải công nghiệp QCVN 40:2025/BTNMT & lộ trình quan trắc tự động](https://devicelab.vn/kien-thuc/quy-chuan-nuoc-thai-cong-nghiep-qcvn-40-quan-trac-tu-dong/)
- [Data logger nhiệt độ đa kênh PT100 (RTD 3 dây) & bộ ghi nhiệt độ công nghiệp](https://devicelab.vn/kien-thuc/data-logger-nhiet-do-da-kenh-pt100-bo-ghi-nhiet-do-cong-nghiep/)
- [Tủ RTU & Thiết bị Remote Terminal Unit SCADA cho nhà máy nước, thủy điện](https://devicelab.vn/kien-thuc/tu-rtu-thiet-bi-remote-terminal-unit-scada-nha-may-nuoc-thuy-dien/)
- [Hệ thống quan trắc nước ngầm tự động giếng khoan chuẩn Nghị định 53/2024/NĐ-CP](https://devicelab.vn/kien-thuc/he-thong-quan-trac-nuoc-ngam-tu-dong/)
- [Giải pháp thay thế Datalogger Campbell Scientific CR1000X / CR300 OEM Việt Nam](https://devicelab.vn/kien-thuc/giai-phap-thay-the-datalogger-campbell-cr1000x-cr300-oem-viet-nam/)
- [Circular 10 Environmental Monitoring Datalogger Solution (English)](https://devicelab.vn/en/environmental-monitoring-datalogger/)

### 3. 3-Phase Power Metering, Solar Zero Export & PLC OEE Telemetry
- [Hệ thống giám sát điện năng nhà máy 3 pha & quản lý năng lượng EMS ISO 50001](https://devicelab.vn/giam-sat-dien-nang-nha-may/)
- [Hướng dẫn chọn đồng hồ đo điện 3 pha RS485 Modbus & thanh ghi chuẩn](https://devicelab.vn/kien-thuc/dong-ho-do-dien-3-pha-rs485-giam-sat-dien-nang/)
- [Bộ điều khiển công suất phát PPC, SmartLogger 3000 & Zero Export SCADA EVN](https://devicelab.vn/kien-thuc/bo-dieu-khien-cong-suat-phat-ppc-smartlogger-3000-zero-export-evn/)
- [Thiết bị thu thập dữ liệu PLC (Siemens, Mitsubishi, Delta) & IoT Gateway](https://devicelab.vn/kien-thuc/thiet-bi-thu-thap-du-lieu-plc-iot-gateway/)
- [Hệ thống giám sát máy móc sản xuất Andon OEE thời gian thực](https://devicelab.vn/kien-thuc/he-thong-giam-sat-may-moc-san-xuat-andon-oee/)

### 4. Custom PCB Design, Turnkey PCBA SMT & Embedded Firmware R&D (Hanoi, Vietnam)
- [Dịch vụ thiết kế mạch điện tử theo yêu cầu & phát triển phần cứng công nghiệp](https://devicelab.vn/thiet-ke-mach-dien-tu/)
- [Công ty thiết kế mạch điện tử tại Hà Nội: Năng lực Lab R&D, EMC & Sản xuất OEM](https://devicelab.vn/kien-thuc/cong-ty-thiet-ke-mach-dien-tu-ha-noi/)
- [Dịch vụ thiết kế PCB 2-8 lớp & vẽ mạch nguyên lý chuẩn IPC-2221](https://devicelab.vn/kien-thuc/dich-vu-thiet-ke-pcb/)
- [Quy trình đặt làm mạch điện tử theo yêu cầu từ EVT/DVT đến sản xuất hàng loạt](https://devicelab.vn/kien-thuc/lam-mach-dien-tu-theo-yeu-cau/)
- [Gia công PCB & hàn mạch điện tử SMT (PCBA) trọn gói tại Việt Nam](https://devicelab.vn/gia-cong-pcb/)
- [Dịch vụ lập trình Firmware nhúng (STM32, ESP32, FreeRTOS, Embedded Linux)](https://devicelab.vn/phat-trien-firmware/)
- [Công ty lập trình nhúng, Firmware & IoT công nghiệp tại Việt Nam](https://devicelab.vn/kien-thuc/cong-ty-lap-trinh-nhung-firmware-iot/)
- [Custom PCB Design & Turnkey Electronics Engineering in Vietnam (English)](https://devicelab.vn/en/custom-pcb-design/)

### 5. Community Engineering Publications (Viblo, Dev.to & Tinh Tế)
- [Viblo: Kỹ thuật chống nhiễu RS485, tính toán Bias & cách ly 2500Vrms](https://viblo.asia/p/ky-thuat-chong-nhieu-rs485-trong-nha-may-tinh-toan-dien-tro-pull-uppull-down-va-cach-ly-quang-2500vrms-bA46807wLKv)
- [Viblo: Kiến trúc Store-and-Forward & Ring-Buffer Flash cho Datalogger Thông tư 10](https://viblo.asia/p/kien-truc-store-and-forward-cho-datalogger-quan-trac-moi-truong-thong-tu-102021tt-btnmt-chong-mat-du-lieu-khi-dut-cap-4g-kNLr3eobVgA)
- [Viblo: Đọc đồng hồ điện 3 pha Selec, Schneider, Eastron qua RS485 & MQTT](https://viblo.asia/p/doc-dong-ho-dien-3-pha-selec-schneider-eastron-qua-modbus-rtu-va-day-mqtt-len-cloud-bang-python-c-OXLA0WqvJGr)
- [Viblo: Checklist 12 điểm kiểm tra Schematic & Layout PCB công nghiệp vượt chuẩn EMC](https://viblo.asia/p/checklist-12-diem-kiem-tra-schematic-layout-pcb-cong-nghiep-truoc-khi-gui-fab-de-vuot-bai-test-emc-iec-61000-4-wd43EXawLX9)
- [Dev.to: Designing Industrial RS485 Circuits for High-EMI Factory Environments](https://dev.to/devicelabvn/designing-industrial-rs485-circuits-for-high-emi-factory-environments-2500vrms-isolation-600w-2114)
- [Dev.to: Store-and-Forward Telemetry Architecture for Environmental Monitoring Dataloggers](https://dev.to/devicelabvn/store-and-forward-telemetry-architecture-for-environmental-monitoring-dataloggers-circular-4b2i)
