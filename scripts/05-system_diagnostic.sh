#!/usr/bin/env bash
set -u

echo "=== DATE ==="
date

echo "=== LOAD ==="
uptime

echo "=== MEMORY ==="
free -h

echo "=== DISK ==="
df -hT /

echo "=== TEMPERATURE ==="
sensors 2>/dev/null || true

echo "=== D-STATE ==="
ps -eo pid,ppid,stat,wchan:40,comm,args | awk '$3 ~ /^D/' || true

echo "=== TOP CPU ==="
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -20

echo "=== KERNEL WARNINGS ==="
journalctl -k -b -p warning..alert --no-pager | tail -100
