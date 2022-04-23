YDots
====
# Presentation
YDots is a dotfiles management system allowing to manage dotfiles using a Yaml configuration file.

# Installation
Run `sudo make`.

# Configuration format
## First run
If you want YDots to manage its own configuration file, run `ydots -c <config.yaml>` once,
with ydots as a module in your configuration file, setup so that it will install the configuration 
file to `XDG_CONFIG_HOME/ydots/config.yaml`, `~/.config/ydots/config.yaml` or `~/ydots/config.yaml`.

For YDots to install packages, use the `-i` flag.

## Next runs
Simply run `ydots` to update all configuration files.
