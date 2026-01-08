#!/bin/bash

# Configuration
MQTT_HOST="mqtt_broker"
SOURCE_TOPIC="home/power/tv"
TARGET_TOPIC="zigbee2mqtt/tv/set"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting MQTT TV Relay... ${NC}"
echo "Listening on: $SOURCE_TOPIC"
echo "Publishing to: $TARGET_TOPIC"
echo "MQTT Host: $MQTT_HOST"
echo "---"

# Subscribe to the source topic and process messages
mosquitto_sub -h "$MQTT_HOST" -t "$SOURCE_TOPIC" | while read -r payload
do
    # Extract the state from the JSON payload
    state=$(echo "$payload" | grep -o '"state":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$state" ]; then
        if [ "$state" = "ON" ]; then
            echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Received ON - Turning TV ON${NC}"
            mosquitto_pub -h "$MQTT_HOST" -t "$TARGET_TOPIC" -m '{"state":"ON"}'
        elif [ "$state" = "OFF" ]; then
            echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Received OFF - Turning TV OFF${NC}"
            mosquitto_pub -h "$MQTT_HOST" -t "$TARGET_TOPIC" -m '{"state":"OFF"}'
        else
            echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Unknown state: $state${NC}"
        fi
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Received invalid payload:  $payload${NC}"
    fi
done
