#!/usr/bin/bash

~/risingwave

sleep 5

docker run --rm \
  -e EVENTS_API_RW_DSN=postgres://root:@localhost:4566/dev \
  -p 8000:8000 \
  --name events-api \
  risingwavelabs/events-api:v0.1.3