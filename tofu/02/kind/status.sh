#!/bin/bash
set -e

if kind get clusters -q | grep -q open-pipeline; then
  status=true
else
  status=false
fi

echo "{\"status\": \"${status}\"}"
