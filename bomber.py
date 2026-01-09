#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = f"""
{Fore.CYAN}+{'='*70}+
|{' '*70}|
|  {Fore.RED}███╗   ███╗{Fore.YELLOW}██████╗  {Fore.GREEN}██████╗ {Fore.CYAN}███╗   ███╗{Fore.MAGENTA}██████╗ {Fore.CYAN}              |
|  {Fore.RED}████╗ ████║{Fore.YELLOW}██╔══██╗{Fore.GREEN}██╔═══██╗{Fore.CYAN}████╗ ████║{Fore.MAGENTA}██╔══██╗{Fore.CYAN}             |
|  {Fore.RED}██╔████╔██║{Fore.YELLOW}██████╔╝{Fore.GREEN}██║   ██║{Fore.CYAN}██╔████╔██║{Fore.MAGENTA}██████╔╝{Fore.CYAN}             |
|  {Fore.RED}██║╚██╔╝██║{Fore.YELLOW}██╔══██╗{Fore.GREEN}██║   ██║{Fore.CYAN}██║╚██╔╝██║{Fore.MAGENTA}██╔══██╗{Fore.CYAN}             |
|  {Fore.RED}██║ ╚═╝ ██║{Fore.YELLOW}██████╔╝{Fore.GREEN}╚██████╔╝{Fore.CYAN}██║ ╚═╝ ██║{Fore.MAGENTA}██████╔╝{Fore.CYAN}             |
|  {Fore.RED}╚═╝     ╚═╝{Fore.YELLOW}╚═════╝ {Fore.GREEN} ╚═════╝ {Fore.CYAN}╚═╝     ╚═╝{Fore.MAGENTA}╚═════╝ {Fore.CYAN}             |
|{' '*70}|
|       {Fore.WHITE}>>> Developer by Manish Kumar v{__VERSION__} <<<{Fore.CYAN}              |
|{' '*70}|
|  {Fore.GREEN}#####{Fore.YELLOW}#####{Fore.RED}#####{Fore.MAGENTA}#####{Fore.CYAN}Manish{Fore.WHITE}..{Fore.GREEN}Kumar{Fore.YELLOW}#####{Fore.RED}#####{Fore.MAGENTA}#####{Fore.CYAN}#####  |
|{' '*70}|
+{'='*70}+{RESET_ALL}
"""
    if ASCII_MODE:
        logo = f"\n{Fore.CYAN}===== MBomb v{__VERSION__} ====={RESET_ALL}\n"
    contributors = "Contributors: "+" ".join(__CONTRIBUTORS__)
    print(logo)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Poor internet connection detected")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False
    if DEBUG_MODE:
        zip_url = "https://github.com/manigpj/MBomb/archive/dev.zip"
        dir_name = "MBomb-dev"
    else:
        zip_url = "https://github.com/manigpj/MBomb/archive/master.zip"
        dir_name = "MBomb-master"
    print(ALL_COLORS[0]+"Downloading ZIP ... "+RESET_ALL)
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_content = response.content
        try:
            with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
                for member in zip_file.namelist():
                    filename = os.path.split(member)
                    if not filename[1]:
                        continue
                    new_filename = os.path.join(
                        filename[0].replace(dir_name, "."),
                        filename[1])
                    source = zip_file.open(member)
                    target = open(new_filename, "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
            success = True
        except Exception:
            mesgdcrt.FailureMessage("Error occured while extracting !!")
    if success:
        mesgdcrt.SuccessMessage("MBomb was updated to the latest version")
        mesgdcrt.GeneralMessage(
            "Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update MBomb.")
        mesgdcrt.WarningMessage(
            "Grab The Latest one From https://github.com/manigpj/MBomb.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("MBomb was updated to the latest version")
        mesgdcrt.GeneralMessage(
            "Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update MBomb.")
        mesgdcrt.WarningMessage("Make Sure To Install 'git' ")
        mesgdcrt.GeneralMessage("Then run command:")
        print(
            "git checkout . && "
            "git pull https://github.com/manigpj/MBomb.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()


def check_for_updates():
    if DEBUG_MODE:
        mesgdcrt.WarningMessage(
            "DEBUG MODE Enabled! Auto-Update check is disabled.")
        return
    try:
        mesgdcrt.SectionMessage("Checking for updates")
        fver = requests.get(
            "https://raw.githubusercontent.com/manigpj/MBomb/master/.version",
            timeout=5
        ).text.strip()
        if fver != __VERSION__:
            mesgdcrt.WarningMessage("An update is available")
            mesgdcrt.GeneralMessage("You can update manually if needed")
        else:
            mesgdcrt.SuccessMessage("MBomb is up-to-date")
    except Exception:
        mesgdcrt.WarningMessage("Could not check for updates - Skipping...")
    mesgdcrt.GeneralMessage("Starting MBomb")


def notifyen():
    try:
        if DEBUG_MODE:
            url = "https://github.com/manigpj/MBomb/raw/dev/.notify"
        else:
            url = "https://github.com/manigpj/MBomb/raw/master/.notify"
        noti = requests.get(url).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("NOTIFICATION: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "Enter your country code (Without +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "The country code ({cc}) that you have entered"
                " is invalid or unsupported".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "Enter the target number: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "The phone number ({target})".format(target=target) +
                "that you have entered is invalid")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Enter target mail: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "The mail ({target})".format(target=target) +
                " that you have entered is invalid")
            continue
        return target


def pretty_print(cc, target, success, failed, total, start_time):
    """Ultra-advanced pretty print with animated progress bar."""
    elapsed = time.time() - start_time
    speed = (success + failed) / elapsed if elapsed > 0 else 0
    eta = (total - success) / speed if speed > 0 else 0
    
    # Progress bar with gradient colors
    progress_pct = (success / total) * 100 if total > 0 else 0
    bar_width = 35
    filled = int((success / total) * bar_width) if total > 0 else 0
    
    if progress_pct < 33:
        bar_color = Fore.RED
    elif progress_pct < 66:
        bar_color = Fore.YELLOW
    else:
        bar_color = Fore.GREEN
    
    progress_bar = f"{bar_color}{'#' * filled}{Fore.WHITE}{'-' * (bar_width - filled)}{RESET_ALL}"
    speed_fire = ">>>" if speed > 5 else ">>" if speed > 2 else ">" if speed > 0 else ""
    
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{Fore.WHITE}        <<< MBOMB TURBO ATTACK IN PROGRESS >>>        {Fore.CYAN}|{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Target     : {Fore.YELLOW}+{cc} {target}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Progress   : [{progress_bar}] {progress_pct:.1f}%")
    print(f"{Fore.CYAN}|{RESET_ALL}  Status     : {Fore.GREEN}OK:{success}{RESET_ALL} / {Fore.RED}FAIL:{failed}{RESET_ALL} / Total:{total}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Speed      : {Fore.MAGENTA}{speed:.1f} req/sec{RESET_ALL} {speed_fire}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Time       : {Fore.BLUE}{elapsed:.1f}s{RESET_ALL} (ETA: {eta:.1f}s)")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.YELLOW}|  WARNING: Educational Purposes Only!{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")


def workernode(mode, cc, target, count, delay, max_threads):
    """Ultra-fast worker with turbo mode."""
    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    
    # Turbo banner
    print(f"""
{Fore.CYAN}+{'='*60}+
|{Fore.RED}#####{Fore.YELLOW}#####{Fore.GREEN}#####{Fore.CYAN}#####{Fore.MAGENTA}#####{Fore.WHITE}#####{Fore.CYAN}######################|
|                                                            |
|  {Fore.WHITE}>>> HYPER-TURBO MODE ACTIVATED <<<{Fore.CYAN}                      |
|                                                            |
|{Fore.RED}#####{Fore.YELLOW}#####{Fore.GREEN}#####{Fore.CYAN}#####{Fore.MAGENTA}#####{Fore.WHITE}#####{Fore.CYAN}######################|
+{'='*60}+{RESET_ALL}
""")
    
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{Fore.WHITE}                 MISSION BRIEFING                         {Fore.CYAN}|{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  API Version   : {Fore.GREEN}{api.api_version}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Target        : {Fore.YELLOW}+{cc} {target}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Payload       : {Fore.MAGENTA}{count} {mode.upper()}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Threads       : {Fore.RED}{max_threads} (TURBO){RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Delay         : {Fore.BLUE}{delay}s{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  APIs Ready    : {Fore.GREEN}{len(APIProvider.api_providers)}{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}WARNING: This tool is for educational purposes only!{RESET_ALL}")
    print()
    input(f"{Fore.GREEN}>> {Fore.WHITE}Press {Fore.CYAN}[ENTER]{Fore.WHITE} to {Fore.RED}LAUNCH ATTACK{Fore.WHITE} >> {RESET_ALL}")

    if len(APIProvider.api_providers) == 0:
        print(f"{Fore.RED}ERROR: Your country/target is not supported yet{RESET_ALL}")
        input(f"{Fore.GREEN}>> {Fore.WHITE}Press [ENTER] to exit{RESET_ALL}")
        bann_text()
        sys.exit()

    success, failed = 0, 0
    start_time = time.time()
    
    while success < count:
        batch_size = min(count - success, max_threads * 3)
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = [executor.submit(api.hit) for _ in range(batch_size)]

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    clr()
                    print(f"{Fore.RED}+{'='*60}+")
                    print(f"|           RATE LIMIT REACHED!                            |")
                    print(f"+{'='*60}+{RESET_ALL}")
                    print(f"{Fore.YELLOW}Final: {success} sent | {failed} failed{RESET_ALL}")
                    input(f"{Fore.GREEN}>> Press [ENTER] to exit{RESET_ALL}")
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed, count, start_time)
    
    # Completion
    elapsed = time.time() - start_time
    avg_speed = success / elapsed if elapsed > 0 else 0
    
    clr()
    print(f"""
{Fore.GREEN}+{'='*60}+
|  ****************************************************    |
|                                                          |
|       MISSION ACCOMPLISHED - BOMBING COMPLETE!           |
|                                                          |
|  ****************************************************    |
+{'='*60}+{RESET_ALL}
""")
    
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{Fore.WHITE}                 FINAL STATISTICS                        {Fore.CYAN}|{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Successful    : {Fore.GREEN}{success}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Failed        : {Fore.RED}{failed}{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Total Time    : {Fore.BLUE}{elapsed:.2f}s{RESET_ALL}")
    print(f"{Fore.CYAN}|{RESET_ALL}  Avg Speed     : {Fore.MAGENTA}{avg_speed:.2f} req/sec{RESET_ALL}")
    if (success+failed) > 0:
        print(f"{Fore.CYAN}|{RESET_ALL}  Success Rate  : {Fore.GREEN}{(success/(success+failed))*100:.1f}%{RESET_ALL}")
    print(f"{Fore.CYAN}+{'='*60}+{RESET_ALL}")
    
    print()
    print(f"{Fore.YELLOW}Thanks for using MBomb! Stay safe.{RESET_ALL}")
    time.sleep(3)
    bann_text()
    sys.exit()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Enter number of {type}".format(type=mode.upper()) +
                           " to send (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("You have requested " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Automatically capping the value"
                        " to {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("Enter delay time (in seconds): "))
                    .strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "Enter Number of Thread (Recommended: {max_limit}): "
                        .format(max_limit=max_thread_limit)))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Read Instructions Carefully !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("MBomb will work only in Python v3")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['MBomb', 't0xic0der', 'scpketer', 'Stefan']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

ASCII_MODE = False
DEBUG_MODE = False

description = """MBomb - Your Friendly Spammer Application

MBomb can be used for many purposes which incudes -
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....

MBomb is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Coded by MBomb !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="start MBomb with SMS Bomb mode")
parser.add_argument("-call", "--call", action="store_true",
                    help="start MBomb with CALL Bomb mode")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="start MBomb with MAIL Bomb mode")
parser.add_argument("-ascii", "--ascii", action="store_true",
                    help="show only characters of standard ASCII set")
parser.add_argument("-u", "--update", action="store_true",
                    help="update MBomb")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current MBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="show current MBomb version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.ascii:
        ASCII_MODE = True
        mesgdcrt = MessageDecorator("stat")
    if args.version:
        print("Version: ", __VERSION__)
    elif args.contributors:
        print("Contributors: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {
            "1": "SMS",
            "2": "CALL",
            "3": "MAIL"
        }
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print(f"""
{Fore.CYAN}+{'='*55}+
|{Fore.RED}  ╔═╗╔═╗╦  ╔═╗╔═╗╔╦╗  {Fore.YELLOW}╦ ╦╔═╗╦ ╦╦═╗  {Fore.GREEN}╦ ╦╔═╗╔═╗╔═╗╔═╗╔╗╔{Fore.CYAN}  |
|{Fore.RED}  ╚═╗║╣ ║  ║╣ ║   ║   {Fore.YELLOW}╚╦╝║ ║║ ║╠╦╝  {Fore.GREEN}║║║║╣ ╠═╣╠═╝║ ║║║║{Fore.CYAN}  |
|{Fore.RED}  ╚═╝╚═╝╩═╝╚═╝╚═╝ ╩   {Fore.YELLOW} ╩ ╚═╝╚═╝╩╚═  {Fore.GREEN}╚╩╝╚═╝╩ ╩╩  ╚═╝╝╚╝{Fore.CYAN}  |
+{'='*55}+{RESET_ALL}""")
                print(f"{Fore.CYAN}|{RESET_ALL}")
                print(f"{Fore.CYAN}|  {Fore.GREEN}[1]{RESET_ALL} {Fore.RED}>>>{Fore.YELLOW} SMS BOMBER   {Fore.WHITE}- Unleash SMS Storm{RESET_ALL}")
                print(f"{Fore.CYAN}|  {Fore.GREEN}[2]{RESET_ALL} {Fore.RED}>>>{Fore.YELLOW} CALL BOMBER  {Fore.WHITE}- Ring of Chaos{RESET_ALL}")
                print(f"{Fore.CYAN}|  {Fore.GREEN}[3]{RESET_ALL} {Fore.RED}>>>{Fore.YELLOW} MAIL BOMBER  {Fore.WHITE}- Email Warfare{RESET_ALL}")
                print(f"{Fore.CYAN}|{RESET_ALL}")
                print(f"{Fore.CYAN}+{'='*55}+{RESET_ALL}")
                print(f"{Fore.MAGENTA}|  Developer: Manish Kumar{RESET_ALL}")
                print(f"{Fore.CYAN}+{'='*55}+{RESET_ALL}")
                print()
                choice = input(f"{Fore.GREEN}>> {Fore.WHITE}Choose Weapon {Fore.CYAN}[1-3]{Fore.WHITE}: {RESET_ALL}")
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    sys.exit()
