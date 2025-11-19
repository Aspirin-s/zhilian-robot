#!/bin/bash
# wait-for-it.sh - 等待服务就绪的脚本

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

until nc -z "$host" "$port"; do
  >&2 echo "等待 $host:$port 就绪..."
  sleep 1
done

>&2 echo "$host:$port 已就绪"
exec $cmd
