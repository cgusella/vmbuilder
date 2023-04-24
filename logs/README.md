
---

## put this code in .bashrc to activate logs

```
# Packer log settings

# get current date-time
_now=$(date +"%Y%m%d_%H%M%S")

export PACKER_LOG=1
export PACKER_LOG_PATH="logs/build_$_now.log"
```
---
