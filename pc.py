#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# opensquat.py
"""
openSquat.

* https://github.com/atenreiro/opensquat

software licensed under GNU version 3
"""
import time
import signal
import functools
import concurrent.futures

from colorama import init, Fore, Style
from opensquat import __VERSION__, vt
from opensquat import arg_parser, output, app, phishing, check_update

from opensquat import port_check


def signal_handler(sig, frame):
    """Function to catch CTR+C and terminate."""
    print("\n[*] openSquat is terminating...\n")
    exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    init()

    RED, WHITE, GREEN, END, YELLOW, BOLD = (
        "\033[91m",
        "\33[97m",
        "\033[1;32m",
        "\033[0m",
        "\33[93m",
        "\033[1m",
    )

    logo = (
        Style.BRIGHT + Fore.GREEN +
        """
                                             █████████                                  █████
                                            ███░░░░░███                                ░░███
      ██████  ████████   ██████  ████████  ░███    ░░░   ████████ █████ ████  ██████   ███████
     ███░░███░░███░░███ ███░░███░░███░░███ ░░█████████  ███░░███ ░░███ ░███  ░░░░░███ ░░░███░
    ░███ ░███ ░███ ░███░███████  ░███ ░███  ░░░░░░░░███░███ ░███  ░███ ░███   ███████   ░███
    ░███ ░███ ░███ ░███░███░░░   ░███ ░███  ███    ░███░███ ░███  ░███ ░███  ███░░███   ░███ ███
    ░░██████  ░███████ ░░██████  ████ █████░░█████████ ░░███████  ░░████████░░████████  ░░█████
     ░░░░░░   ░███░░░   ░░░░░░  ░░░░ ░░░░░  ░░░░░░░░░   ░░░░░███   ░░░░░░░░  ░░░░░░░░    ░░░░░
              ░███                                          ░███
              █████                                         █████
             ░░░░░                                         ░░░░░
                    (c) Andre Tenreiro - https://github.com/atenreiro/opensquat
    """ + Style.RESET_ALL
    )

    print(logo)
    print("\t\t\tversion " + __VERSION__ + "\n")

    args = arg_parser.get_args()

    start_time_squatting = time.time()

    file_content = app.Domain().main(
        args.keywords,
        args.confidence,
        args.domains,
        args.period,
        args.method,
        args.dns,
        args.ct
    )

    
    
   
    # Check if domain has webserver port opened
    if (args.portcheck):
        list_aux = []
        print("\n+---------- Domains with open webserver ports ----------+")
        time.sleep(1)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futs = [ (domain, executor.submit(functools.partial(port_check.PortCheck().main, domain)))
                for domain in file_content ]
        
        for tested_domain, result_domain_port_check in futs:
            ports = result_domain_port_check.result()
            if ports:
                list_aux.append(tested_domain)
                print(
                    Fore.YELLOW +
                    "[*]", tested_domain, ports, "" +
                    Style.RESET_ALL
                    )
        
        file_content = list_aux
        print("[*] Total found:", len(file_content))

    output.SaveFile().main(args.output, args.type, file_content)
    end_time_squatting = round(time.time() - start_time_squatting, 2)

    # Print summary
    print("\n")
    print(
        Style.BRIGHT+Fore.GREEN +
        "+---------- Summary Squatting ----------+" +
        Style.RESET_ALL)

    print("[*] Domains flagged:", len(file_content))
    print("[*] Domains result:", args.output)

    

    print("[*] Running time: %s seconds" % end_time_squatting)
    print("")

    check_update.CheckUpdate().main()
