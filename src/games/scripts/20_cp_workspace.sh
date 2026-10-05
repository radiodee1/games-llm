#!/bin/bash

if [ -d "/workspace" ]; then
  echo 'copy to workspace'
  cp -r ~/workspace/* /workspace
else
  echo 'no workspace for copy'
fi
