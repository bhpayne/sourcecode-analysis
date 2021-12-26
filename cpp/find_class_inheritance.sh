#!/usr/bin/env bash


find ../../../sstsimulator/ -type f -name "*.c*" | xargs grep "^\s*class.*:"
