#!/bin/bash
# Script to automatically update mobile app with current IP address

# Get current IP address
CURRENT_IP=$(ipconfig | grep "Wireless LAN adapter Wi-Fi" -A 5 | grep "IPv4" | awk '{print $NF}')

if [ -z "$CURRENT_IP" ]; then
    echo "❌ Could not detect IP address"
    exit 1
fi

echo "🔍 Detected IP: $CURRENT_IP"

# Update apiConstants.js
sed -i "s|BASE_URL: 'http://[0-9.]*:8000'|BASE_URL: 'http://$CURRENT_IP:8000'|g" Mobile/src/services/apiConstants.js

# Update api.js
sed -i "s|baseURL: 'http://[0-9.]*:8000'|baseURL: 'http://$CURRENT_IP:8000'|g" Mobile/src/utils/api.js

echo "✅ Updated mobile config to: http://$CURRENT_IP:8000"
echo ""
echo "📱 Now reload your app (press 'r' in Metro bundler)"
