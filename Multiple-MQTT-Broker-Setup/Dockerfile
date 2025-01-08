# Use the official Eclipse Mosquitto image as the base image
FROM eclipse-mosquitto

# Copy configuration file to mosquitto config directory
COPY broker.conf /mosquitto/config/

# Expose Mosquitto port
EXPOSE 1883

# Start the MQTT broker
CMD ["mosquitto", "-c", "/mosquitto/config/broker.conf"] 
