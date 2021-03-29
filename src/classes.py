#!/usr/bin/env python3

import argparse
import datetime
import os
import re
import requests
import sys

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from outbreaker.utils import binary_query, int_query

# TODO:
# - Replace print statements with a logger, retain colourisation if possible
# - Determine method for running outbreaker daily or something to alert in terminal each morning?
#   - ie. set up alert system


class outbreakerClass(object):
    """docstring for outbreaker"""
    def __init__(self):
        self.language = 'en'
        self.coreURL = 'http://www.who.int'
        self.latestURL = f"{self.coreURL}/csr/don/{self.language}/"
        self.outformat = '\033[94m[{0:}] \033[92m[{1}]\033[0m: {2:}: \033[90m{3:}\033[0m' # [Index] [Date]: Title: Link
        self.titleFormat = '\033[1m-{0}-\033[0m'

    def run(self):
        self.args = self.setup_parser()

        if self.args.command == 'latest':
            if self.args.verbose:
                self.info('Finding latest reports...')
                self.getLatest()
        elif self.args.command == 'archive':
            if self.args.verbose:
                self.info('Fetching archived reports...')
            self.getArchive(searchTerm=self.args.searchTerm, recordType=self.args.recordType)
        elif self.args.command == 'download':
            if self.args.verbose:
                print('Downloading report...')
            self.accessReport(url=self.args[1], mode='download', docPerLine=self.args.docPerLine)
        elif self.args.command == 'read':
            if self.args.verbose:
                print('Opening report...')
            self.accessReport(url=self.args[1], mode='read')

    def setup_parser(self):
        parser = argparse.ArgumentParser(description='Outbreaker: An Unofficial WHO Disease Outbreak News API')
        subparsers = parser.add_subparsers(dest='command', help='Sub-command to perform.')


        help_text = {
            'latest': 'Display latest outbreak reports.',
            'archive': 'Search the archives by year, country, or disease.',
            'download': 'Download a specific report.',
            'read': 'Read a specific report.'
        }

        parser_latest = subparsers.add_parser('latest', help=f"{help_text['latest']}", description=f"{help_text['latest']}")
        parser_latest.add_argument('--verbose', action='store_false')

        parser_archive = subparsers.add_parser('archive', help=f"{help_text['archive']}", description=f"{help_text['archive']}")
        parser_archive.add_argument('recordType', choices=['year', 'disease', 'country'], help='Sub-archive to explore.')
        parser_archive.add_argument('searchTerm', nargs='*', help='Term to search for.')
        parser_archive.add_argument('--docPerLine', action='store_true', help=argparse.SUPPRESS)
        parser_archive.add_argument('--filename', default='documents.txt', help=argparse.SUPPRESS)
        parser_archive.add_argument('--verbose', action='store_false')

        parser_download = subparsers.add_parser('download', help=f"{help_text['download']}", description=f"{help_text['download']}")
        parser_download.add_argument('url', help='URL for a WHO report.')
        parser_download.add_argument('--docPerLine', action='store_true', help=argparse.SUPPRESS)
        parser_download.add_argument('--filename', default='documents.txt', help=argparse.SUPPRESS)
        parser_download.add_argument('--verbose', action='store_false')

        parser_read = subparsers.add_parser('read', help=f"{help_text['read']}", description=f"{help_text['read']}")
        parser_read.add_argument('url', help='URL for a WHO report.')
        parser_read.add_argument('--verbose', action='store_false')

        args = parser.parse_args()

        if not args.command:
            parser.print_help(sys.stderr)
            sys.exit(1)

        return(args)

    def setup_logger(self):
        raise NotImplementedError

    def info(self, message):
        print('\033[92m{}\033[0m'.format(message))

    def warn(self, message):
        print('\033[93mWarning: {}\033[0m'.format(message))

    def error(self, message):
        print('\033[91mError: {}\033[0m'.format(message))

    def print_columns(self, text, columns=2, width=20):
        if len(text) % columns != 0:
            text.append(" ")

        split = int(len(text)/columns)
        col_array = []
        start = 0
        for col_n in range(columns):
            col_array.append(text[start:start+split])
            start += split

        for row in zip(*col_array):
            print("".join(str.ljust(i,width) for i in row))

    def list_archive(self, which=None, exit=False):
        if which.lower() == 'year':
            print('Usage: outbreaker.py archive year <year>')
            print('Available Years:')
            self.print_columns(sorted(self.yearDict().keys()), columns=1)
        elif which.lower() == 'disease':
            print('Usage: outbreaker.py archive disease <disease>')
            print('Available Diseases:')
            self.print_columns(sorted(self.diseaseDict().keys(), key=str.casefold), columns=1)
        elif which.lower() == 'country':
            print('Usage: outbreaker archive country <country>')
            print('Available Countries:')
            self.print_columns(sorted(self.countryDict().keys(), key=str.casefold), columns=1)
        else:
            self.error(f"Help type {which} not recognised.")
            sys.exit()
        if exit:
            sys.exit()

    def accessReport(self, article, mode, incImages=True, docPerLine=False):
        url = article['url']
        if self.coreURL not in url:
            self.error("Provided url is not from a recognised domain.")
            sys.exit(-1)
        article_text = BeautifulSoup(requests.get(url).content, 'lxml')
        copy = article_text.find_all('div', id='primary')[0].text
        copy = re.sub(f"{os.linesep}+", os.linesep, copy)
        copy = re.sub(r"\s+", r' ', copy)

        if mode.lower() == 'download':
            filename = url.split('/')[-3]+'.txt' if not docPerLine else self.args.filename
            print('Downloading {0} to {1}'.format(url, filename))
            if docPerLine:
                with open(filename,'a') as f:
                    f.write(f"{article['date']} |{copy.replace(os.linesep,' ').replace('  ',' ')+os.linesep}")
            else:
                with open(filename,'w') as f:
                    f.write(copy)
        elif mode.lower() == 'read':
            print(copy)
        else:
            self.error(f"Report mode '{mode}' not recognised.")

    def yearDict(self, yearURL='https://www.who.int/csr/don/archive/year/en/'):
        if not hasattr(self, 'years'):
            self.info('Fetching year list...')
            soup = BeautifulSoup(requests.get(yearURL).content,'lxml')
            yearDict = {z.text: z.get('href') for z in [x for y in [d.find_all('a', href=True) for d in soup.find_all('ul', class_='list')[0] if not isinstance(d, NavigableString)] for x in y]}
            return(yearDict)
        else:
            return(self.years)

    def diseaseDict(self, diseaseURL='http://www.who.int/csr/don/archive/disease/en/'):
        if not hasattr(self, 'diseases'):
            self.info('Fetching disease list...')
            soup = BeautifulSoup(requests.get(diseaseURL).content,'lxml')
            diseaseDict = {z.text.upper(): z.get('href') for z in [x for y in [d.find_all('a', href=True) for d in soup.find_all('ul', class_='a_z')] for x in y]}
            return(diseaseDict)
        else:
            return(self.diseases)

    def countryDict(self, countryURL='http://www.who.int/csr/don/archive/country/en/'):
        if not hasattr(self, 'countries'):
            self.info('Fetching country list...',)
            soup = BeautifulSoup(requests.get(countryURL).content,'lxml')

            countryDict = {}
            for d in soup.find_all('ul', class_='a_z'):
                    for y in d.find_all('a', href=True):
                        if (y.text is not None) and (y.get('href') is not None):
                            countryDict[y.text.upper()] = y.get('href')

            return(countryDict)
        else:
            return(self.countries)

    def getLatest(self):
        soup = BeautifulSoup(requests.get(self.latestURL).content, "lxml")

        articles = []
        reports = soup.find_all('ul', class_='auto_archive')
        if len(reports) < 1:
            self.error("No recent reports found.".format(**locals()))
            sys.exit()
        print(self.titleFormat.format('Latest Disease Outbreaks (Source: WHO)'))
        index = 0
        for report in reports[0].find_all('li'):
            index += 1
            date = report.a.text
            title = report.span.text
            url = self.coreURL+report.find_all('a',href=True)[0].get('href')
            articles.append({'date': date, 'title': title, 'url': url})
            print(self.outformat.format(index, date, title, url))

        if binary_query('Download these reports?'):
            for article in articles:
                self.accessReport(article, mode='download')

        articleID = int_query('Read a report?', minVal=1, maxVal=len(articles)) - 1
        if articleID <= len(articles):
            self.accessReport(articles[articleID], mode='read')

    def getArchive(self, searchTerm=None, recordType=None, coreURL=None, language=None):
        if coreURL is None:
            coreURL = self.coreURL
        if language is None:
            language = self.language
        if isinstance(searchTerm, list):
            searchTerm = ' '.join(searchTerm)
        if recordType.lower() == 'year':
            self.years = self.yearDict()
            currentYear = datetime.datetime.now().year
            if searchTerm is None or not searchTerm.isdigit():
                self.list_archive(which='year', exit=True)
            elif int(searchTerm) not in range(1996,currentYear+1):
                self.error("No reports available for the year '{0}'.".format(searchTerm))
                self.list_archive(which='year', exit=True)
            searchTerm_orig = searchTerm
        elif recordType.lower() == 'disease':
            self.diseases = self.diseaseDict()
            if searchTerm is None:
                self.list_archive(which='disease', exit=True)
            elif searchTerm not in self.diseases.keys():
                self.error("Given disease '{}' not found".format(searchTerm))
                self.list_archive(which='disease', exit=True)
            else:
                searchTerm_orig = searchTerm
                searchTerm = self.diseases[searchTerm].split('/')[-2]
                if ' ' in searchTerm: searchTerm = '_'.join(searchTerm.lower().split(' '))
        elif recordType.lower() == 'country':
            self.countries = self.countryDict()
            if searchTerm is None:
                self.list_archive(which='country', exit=True)
            elif searchTerm not in self.countries.keys():
                self.error("Given country '{}' not found".format(searchTerm))
                self.list_archive(which='country', exit=True)
            else:
                searchTerm_orig = searchTerm
                searchTerm = self.countries[searchTerm].split('/')[-2]
                if ' ' in searchTerm:
                    searchTerm = '_'.join(searchTerm.lower().split(' '))
        else:
            self.error('Record type not recognised.')
            sys.exit()

        archiveURL = '{self.coreURL}/csr/don/archive/{recordType}/{0}/{self.language}/'.format(searchTerm, **locals())
        soup = BeautifulSoup(requests.get(archiveURL).content, "lxml")

        if recordType == 'country':
            searchTerm = searchTerm_orig

        articles = []
        reports = soup.find_all('ul', class_='auto_archive')
        if len(reports) < 1:
            self.error("No reports found for '{searchTerm_orig}'".format(**locals()))
            sys.exit(-1)
        print(self.titleFormat.format('Archive Outbreaks For {searchTerm_orig} (Source: WHO)'.format(**locals())))
        index = 0
        for report in reports[0].find_all('li'):
            index += 1
            date = report.a.text
            title = report.span.text
            url = self.coreURL+report.find_all('a',href=True)[0].get('href')
            articles.append({'date': date, 'title': title, 'url': url})
            print(self.outformat.format(index, date, title, url))

        if self.args.docPerLine:
            for article in articles:
                self.accessReport(article, mode='download', docPerLine=self.args.docPerLine)
        else:
            if binary_query('Download these reports?'):
                for article in articles:
                    self.accessReport(article, mode='download', docPerLine=self.args.docPerLine)

            articleID = int_query('Read a report?', minVal=1, maxVal=len(articles)) - 1
            if articleID <= len(articles):
                self.accessReport(articles[articleID], mode='read')
