#!/bin/bash
# Test script for PIE HTTP server

echo "=== Testing PIE HTTP Server ==="
echo ""
echo "1. Testing GET request..."
curl -s http://localhost:9999/
echo ""
echo ""

echo "2. Testing POST request with JSON body..."
curl -s -X POST http://localhost:9999/api/data \
     -H "Content-Type: application/json" \
     -d '{"name": "Ian", "age": 21, "role": "student"}'
echo ""
echo ""

echo "3. Testing POST request with different data..."
curl -s -X POST http://localhost:9999/api/users \
     -H "Content-Type: application/json" \
     -d '{"username": "test123", "email": "test@example.com"}'
echo ""
echo ""

echo "=== Tests completed ==="
