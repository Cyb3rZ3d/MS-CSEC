import argparse
import urllib.request
from urllib.error import URLError, HTTPError

from VulnerabilityScanner.CommonPortsCheck import CommonPortsCheck
from VulnerabilityScanner.Crawler import Crawler
from VulnerabilityScanner.LFIScanner import LfiScanner
from VulnerabilityScanner.ReportGenerator import ReportGenerator
from VulnerabilityScanner.SecurityHeaders import SecurityHeaders
from VulnerabilityScanner.SqlInjection import SqlInjection
from VulnerabilityScanner.XssScanner import XssScanner


def perform_scans(quiet, givenurl, urls, xsspayload, lfi_url, nohttps):
    """
    Function performing scans and executing attacks
    """
    global_vulnerabilities = set()
    # Create report
    report = ReportGenerator(givenurl)
    # Check common ports
    ports = CommonPortsCheck(quiet)
    ports.scan_ports(givenurl, report)
    # Check security headers for main URL
    secheaders = SecurityHeaders(givenurl, quiet, nohttps)
    secheaders.check_security_headers(report)
    # Perform advanced LFI scan if extra URL was provided
    if lfi_url:
        lfi_advanced = LfiScanner(quiet, lfi_url)
        lfi_advanced.advanced_lfi(report)
    # Perform attacks for xss, sqli, and basic lfi
    if urls:
        for url in urls:
            report.write_to_report(f"\n [*****]  Checking URL: {url}  [*****] \n")
            if not quiet:
                print(f"\n [*****]  Checking URL: {url}  [*****] \n")
            attacks(report, url, quiet, xsspayload, global_vulnerabilities)
    else:
        attacks(report, givenurl, quiet, xsspayload, global_vulnerabilities)


def check_lfi_url(url):
    """
    Check if provided URL have specific characters in it
    Args:
        url: URL to be checked

    Returns: True or False
    """
    if '=' in url and '?' in url:
        request_website = urllib.request.urlopen(url).getcode()
        if request_website == 200:
            return True
        else:
            return False


def attacks(report, url, quiet, xsspayload, vulnerability_tracker):
    """
    Execute attacks for provided URL
    """
    # Scan for XSS
    xss_scan = XssScanner(quiet, url, vulnerability_tracker)
    xss_scan.scan_host(report, xsspayload)
    # Check for LFI
    lfi_scan = LfiScanner(quiet, url)
    lfi_scan.basic_scan_host(report)
    # Check for Sql Injections
    sql_inj = SqlInjection(quiet, url)
    sql_inj.scan_host(report)


def main():
    xsspayload = ''
    lfi_url = ''
    urls = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--crawler', help='Crawl to provided depth', dest='crawler',
                        type=int, default=1)
    parser.add_argument('-q', '--quiet', help='quiet mode - no console output generated',
                        dest='quiet', action='store_true')
    parser.add_argument('-u', '--url', help='Provide URL for web application, example: https://www.example.com',
                        required=True, dest='url')
    parser.add_argument('-xp', '--xsspayload', help='Path to XSS payload', dest='xsspayload')
    parser.add_argument('-lu', '--lfiurl', help='Provide url with parameters to perform advanced LFI scan, example:'
                                                'https://www.example.com/page.php?file=', dest='lfi_url')
    parser.add_argument('-nh', '--nohttps', help='Dont check for https header', dest='nohttps', action='store_true')
    arguments = parser.parse_args()

    try:
        check_site = urllib.request.urlopen(arguments.url)
        print("Site responded with code " + str(check_site.getcode()))
    except (HTTPError, URLError) as e:
        print("Connection to: " + arguments.url + " could not be established, error code: " + str(e))
        exit()

    url_len = len(arguments.url)
    if arguments.url[url_len - 1] == '/':
        arguments.url = arguments.url[:-1]
    print(arguments.url)

    if arguments.xsspayload:
        xsspayload = arguments.xsspayload

    if arguments.lfi_url:
        check_url = check_lfi_url(arguments.lfi_url)
        if check_url:
            lfi_url = arguments.lfi_url
        else:
            print("LFI URL doesn't respond, performing scan without advanced lfi")

    if arguments.crawler:
        urls = Crawler.deep_crawl(arguments.url, arguments.crawler)
        if arguments.url not in urls:
            urls.append(arguments.url)

    perform_scans(arguments.quiet, arguments.url, urls, xsspayload, lfi_url, arguments.nohttps)


if __name__ == '__main__':
    main()
