# A semi-automatic parser for [www.mobilesuica.com](www.mobilesuica.com)

## Requirements
- chromedriver - either in `PATH` or set via `SUICA_DRIVER` / `-d <path>`

## Usage
`suicaParse -u username -p password -o history.json`

You can also use the following environment variables instead of options:
- `SUICA_USERNAME`
- `SUICA_PASSWORD`
- `SUICA_DRIVER`

