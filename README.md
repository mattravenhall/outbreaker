# Outbreaker
Unofficial API for the WHO Disease Outbreak News
![Example View](https://raw.githubusercontent.com/mattravenhall/outbreaker/master/media/example.png)

## Overview
The World Health Organisation has an [awesome resource of disease outbreak reports](http://www.who.int/csr/don/en/) that I believe is underutilised. To improve access to this resource, I've developed a small command line package that handles some specific requests.

Currently users are able to pull down the five most recent reports, request the full archive for a given year (from 1996 onwards), country or diseases, and download or read specific articles. In the future I plan to extend *Outbreaker*'s capacities to include features such as outbreak alerts.

Naturally this package relies on the WHO website's existing layout, if anything breaks please highlight it as an issue on the package's [github repo](https://github.com/mattravenhall/outbreaker).

## Installation
### Via pip
`pip install outbreaker`

### Via GitHub
Find the latest release wheel on the [releases tab](https://github.com/mattravenhall/outbreaker/releases/latest).

### Running
Installation will add the *outbreaker* command to your PATH.

### Run Types
- `latest` Return the dates, titles, and urls for the five most recent reports.
- `archive <year/country/disease>` Return a list of the reports found in the given year, country, or disease.
- `download <report_url>` Download a given article url as a .txt file (nb. this has not yet been optimised for all articles).
- `read <report_url>` Print out a given article to the terminal.
