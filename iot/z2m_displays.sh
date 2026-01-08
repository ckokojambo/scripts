#!/bin/bash

# Configuration
MQTT_HOST="mqtt_broker"
SOURCE_TOPIC="home/power/displays"

# Target outlets configuration
POWERSTRIP1_TOPIC="zigbee2mqtt/powerstrip1/set"
POWERSTRIP2_TOPIC="zigbee2mqtt/powerstrip2/set"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting MQTT Displays Relay... ${NC}"
echo "Listening on: $SOURCE_TOPIC"
echo "Publishing to:"
echo "  - $POWERSTRIP1_TOPIC (L1, L2, L3)"
echo "  - $POWERSTRIP2_TOPIC (L1, L2, L3)"
echo "MQTT Host: $MQTT_HOST"
echo "---"

# Subscribe to the source topic and process messages
mosquitto_sub -h "$MQTT_HOST" -t "$SOURCE_TOPIC" | while read -r payload
do
    # Extract the state from the JSON payload
    state=$(echo "$payload" | grep -o '"state":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$state" ]; then
        if [ "$state" = "ON" ]; then
            echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Received ON - Turning displays ON${NC}"
            
            # Turn on powerstrip1 outlets L1, L2, L3
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l1":"ON"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l2":"ON"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l3":"ON"}'
            
            # Turn on powerstrip2 outlets L1, L2, L3
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l1":"ON"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l2":"ON"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l3":"ON"}'
            
            echo -e "${GREEN}  ✓ Powerstrip1: L1, L2, L3 ON${NC}"
            echo -e "${GREEN}  ✓ Powerstrip2: L1, L2, L3 ON${NC}"
            
        elif [ "$state" = "OFF" ]; then
            echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Received OFF - Turning displays OFF${NC}"
            
            # Turn off powerstrip1 outlets L1, L2, L3
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l1":"OFF"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l2":"OFF"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP1_TOPIC" -m '{"state_l3":"OFF"}'
            
            # Turn off powerstrip2 outlets L1, L2, L3
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l1":"OFF"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l2":"OFF"}'
            mosquitto_pub -h "$MQTT_HOST" -t "$POWERSTRIP2_TOPIC" -m '{"state_l3":"OFF"}'
            
            echo -e "${RED}  ✓ Powerstrip1: L1, L2, L3 OFF${NC}"
            echo -e "${RED}  ✓ Powerstrip2: L1, L2, L3 OFF${NC}"
            
        else
            echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Unknown state: $state${NC}"
        fi
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Received invalid payload:  $payload${NC}"
    fi
done
