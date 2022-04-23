YDots
====
# Presentation
YDots is a dotfiles management system allowing to manage dotfiles using a Yaml configuration file.

# Installation
## Requirements
This only requires python>=3.10 and pip.
## Installation
Run `sudo make`.

# Parsing
YDots is able to parse files, replacing occurences of `%{{variable}}` with the value of `variable`
when `file.parse` is set to `true`.

See `config.example.yaml` for details.

# Configuration format
## Example
See `example.config.yaml` for an example configuration file.

## First run
If you want YDots to manage its own configuration file, run `ydots -c <config.yaml>` once,
with ydots as a module in your configuration file, setup so that it will install the configuration 
file to `XDG_CONFIG_HOME/ydots/config.yaml`, `~/.config/ydots/config.yaml` or `~/ydots/config.yaml`.

For YDots to install packages, use the `-i` flag.

## Next runs
Simply run `ydots` to update all configuration files.
