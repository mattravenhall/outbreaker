# Outbreaker
Unofficial API for the WHO Disease Outbreak News

## Overview
The World Health Organisation has an [awesome resource of disease outbreak reports](http://www.who.int/csr/don/en/) which I believe is underutilised. To improve the access to this resource, I've developed a small command line package to handle some specific requests.

Currently users are able to pull down the five most recent reports, request the full archive for a given year (from 1996 onwards), and download specific articles. In the future I plan to extend *Outbreaker*'s capacities to include better data collection (ie. by disease type, better download handling etc.) and outbreak alerts.

Naturally this package relies on the WHO website's existing layout, if anything breaks please highlight it as an issue on the package's [github repo](https://github.com/mattravenhall/outbreaker).

## Technical Details
### Built with:
- bs4 (v4.6.0)
- pandas (v0.19.2)

### First time set-up
Prior to first use it's a good idea to run *preflightchecks.py*. This script will check all required packages are installed, and (optionally, but recommended) add outbreaker to your PATH as a system-wide executable.

### Running
If *Outbreaker* was added to your PATH correctly it can be run with the `outbreaker` command, otherwise the script should be called by its direct path. Calling without arguments will return the help information.

### Run Types
- `latest` Return the dates, titles, and urls for the five most recent reports.
- `archive <year/country/disease>` Return a list of the reports found in the given year, country, or disease.
- `download <report_url>` Download a given article url as a .txt file (nb. this has not yet been optimised for all articles).
