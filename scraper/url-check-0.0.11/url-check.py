#!/usr/bin/env bash
{ set +x; } 2>/dev/null

usage="usage: ${BASH_SOURCE[0]##*/} url"
[[ $# != 1 ]] || [[ $1 == "--help" ]] && {
	echo "$usage"
	[[ $1 == "--help" ]]; exit # exit 0 if --help
}

r="$(curl -I -s "$1")" || exit
[[ $r == *"HTTP/1.1 200 OK"* ]] && exit
echo "$r" | head -1 # output HTTP status
exit 1
# HTTP/1.1 404 Not Found


