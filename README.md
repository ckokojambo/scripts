# Scripts Collection

A curated collection of shell scripts for system setup, IoT automation, monitoring, and various utilities.

## 📁 Repository Structure

```
scripts/
├── install/          # Installation scripts for software and services
├── iot/              # IoT and home automation scripts
├── monitoring/       # Monitoring and observability tools
├── new_setup/        # System setup and configuration scripts
└── tools/            # General utility scripts
```

## 📦 Categories

### 🔧 Installation (`install/`)

**Docker Installation**
- `install_docker.sh` - Automated Docker installation script for Debian-based systems
  - Removes old Docker packages
  - Adds Docker's official GPG key and repository
  - Installs Docker CE, Docker Compose, and related tools
  - Configures user permissions for Docker group

### 🏠 IoT Automation (`iot/`)

MQTT relay scripts for smart home devices using Zigbee2MQTT: 

- `z2m_tv.sh` - TV power control relay
  - Listens on:  `home/power/tv`
  - Controls: `zigbee2mqtt/tv/set`
  
- `z2m_fan.sh` - Fan power control relay
  - Listens on:  `home/power/fan`
  - Controls: `zigbee2mqtt/fan/set`
  
- `z2m_displays.sh` - Multi-display power control
  - Listens on: `home/power/displays`
  - Controls multiple powerstrip outlets (L1, L2, L3 on two powerstrips)

**Features:**
- Real-time MQTT message processing
- Color-coded console output (green/red/yellow)
- Timestamped logging
- JSON payload parsing
- ON/OFF state control

**Requirements:**
- `mosquitto_sub` and `mosquitto_pub` (MQTT clients)
- MQTT broker accessible at hostname `mqtt_broker`

### 📊 Monitoring (`monitoring/`)

**Prometheus Exporters**
- `monitoring/prometheus/exporter/blackbox/install_blackbox.sh`
  - Automated installation of Blackbox Exporter
  - Creates system user and required directories
  - Configures systemd service
  - Sets proper permissions and ownership
  - Usage: `sudo ./install_blackbox.sh [path-to-blackbox_exporter]`

### 🆕 System Setup (`new_setup/`)

- `locales.sh` - System localization configuration
  - Generates German (de_DE.UTF-8) locale
  - Sets regional formats (time, numeric, monetary, etc.)
  - Configures timezone to Europe/Berlin
  - Useful for fresh system installations

### 🛠️ Utilities (`tools/`)

**GPS Data Conversion Scripts**

- `convert_fit_to_gpx.sh` - Batch convert Garmin FIT files to GPX format
  ```bash
  ./convert_fit_to_gpx.sh <input_directory> <output_directory>
  ```

- `convert_fit_to_csv.sh` - Batch convert Garmin FIT files to CSV format
  ```bash
  ./convert_fit_to_csv.sh <input_directory> <output_directory>
  ```

**Features:**
- Batch processing of multiple FIT files
- Automatic output directory creation
- Comprehensive error handling
- CSV export includes:  date, time, lat, lon, altitude, elevation, cadence, speed, temperature

**Requirements:**
- `gpsbabel` - GPS data conversion tool

## 🚀 Quick Start

### Prerequisites

Most scripts require standard Unix utilities.  Additional requirements: 

```bash
# For IoT scripts
sudo apt install mosquitto-clients

# For GPS conversion tools
sudo apt install gpsbabel

# For monitoring scripts
# Download the appropriate exporter binary first
```

### Usage

1. Clone the repository: 
   ```bash
   git clone https://github.com/ckokojambo/scripts.git
   cd scripts
   ```

2. Make scripts executable:
   ```bash
   chmod +x <script-name>. sh
   ```

3. Run the desired script:
   ```bash
   . /<script-name>.sh [arguments]
   ```

## 📝 Script Details

### IoT MQTT Relay Pattern

All IoT scripts follow a common pattern:
- Subscribe to a source MQTT topic
- Parse incoming JSON payloads
- Extract state information (ON/OFF)
- Publish commands to Zigbee2MQTT target topics
- Provide visual feedback with colored output

### Installation Scripts

Installation scripts are designed to be idempotent and can be run multiple times safely.  They typically:
- Check for existing installations
- Create necessary system users and groups
- Set proper file permissions
- Enable and start systemd services

## 🔒 Security Notes

- Installation scripts require root privileges (use `sudo`)
- Review scripts before executing with elevated permissions
- MQTT scripts assume trusted network environment
- Consider implementing MQTT authentication for production use

## 📄 License

This is a personal collection of scripts. Use at your own risk and adapt as needed for your environment. 

## 🤝 Contributing

This is a personal repository, but feel free to fork and adapt these scripts for your own use. 

## ⚠️ Disclaimer

These scripts are provided as-is, without warranty. Always review and test scripts in a safe environment before using them in production. 

---

**Repository:** [ckokojambo/scripts](https://github.com/ckokojambo/scripts)
