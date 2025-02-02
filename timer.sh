#!/bin/sh

counter=${1:-0}  # in seconds
[ ${counter} -eq 0 ] && {
  printf "\n\nUsage: %s N\nwhere N - is number in seconds to countdown\n\n" "${0}"
  exit 1
}

sec2dhms() {
  local ts=$1
  local d=$((ts/60/60/24))
  local h=$((ts/60/60%24))
  local m=$((ts/60%60))
  local s=$((ts%60))
  echo "${d}d  ${h}h  ${m}m  ${s}s"
}

clear
printf "\n\n\n\n\n"
while [ ${counter} -ne 0 ]; do
  figlet "   $(sec2dhms ${counter})"
  printf "${nc}"
  sleep 1
  counter=$((counter-1))
  clear
  printf "\n\n\n\n\n"
done

figlet "   $(sec2dhms ${counter})"
play -n  synth 3 sin 960 synth 3 sin fmod 1920 \
  fade l 0 3 2.8 trim 0 1 repeat 2;
