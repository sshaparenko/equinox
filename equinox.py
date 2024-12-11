import click
import requests
from datetime import datetime


@click.command()
@click.argument("url")
@click.argument("wordlist")
@click.option("-v", "-verbose", is_flag=True, help="verbose mode")
def cli(url: str, wordlist: str, v: bool) -> None:
    """enter point function"""
    print_ascii()

    try:
        check_connection(url)
    except ConnectionError:
        return

    if v:
        check_sqli_verbose(wordlist, url)
        return

    check_sqli(wordlist, url)


def check_connection(url: str):
    print(f"[{now_time()}] [INFO] checking connection to the target URL")
    result = requests.get(url)
    if result.status_code < 200 or result.status_code > 299:
        print(
            f"[{now_time()}] [CRITICAL] unable to connect totarget URL: status code {result.status_code}"
        )
        raise ConnectionError()


def check_sqli(wordlist_path: str, url: str) -> None:
    """function that tests an endpoint for SQL injections"""
    print(f"[{now_time()}] [INFO] trying to inject...")

    injections = read_injections(wordlist_path)
    status_codes = list()

    for inj in injections:
        try:
            injected_url = buildInjection(url, inj)
        except IndexError:
            print(
                f"[{now_time()}] [CRITICAL] could't find any parameter to be injected."
            )
            return
        result = requests.get(injected_url)
        if result.status_code >= 500 or result.status_code <= 599:
            status_codes.append(result)

    if len(status_codes) != 0:
        print(
            f"[{now_time()}] [INFO] parameter '{url.split("?")[1].split("=")[0]}' appears to be vulnerable to SQL injection"
        )
        return

    print(
        f"[{now_time()}] [INFO] parameter '{url.split("?")[1].split("=")[0]}' is not vulnerable to SQL injection"
    )


def check_sqli_verbose(wordlist_path: str, url: str) -> None:
    """function that tests an endpoint for SQL injections"""
    print(f"[{now_time()}] [INFO] trying to inject...")

    injections = read_injections(wordlist_path)
    status_codes = list()

    for inj in injections:
        try:
            injected_url = buildInjection(url, inj)
        except IndexError:
            print(
                f"[{now_time()}] [CRITICAL] could't find any parameter to be injected."
            )
            return
        result = requests.get(injected_url)
        status_codes.append(result)
        print(
            f"[{now_time()}] [INFO] Injection: {inj} Status Code: {result.status_code}"
        )

    if len(status_codes) != 0:
        print(
            f"[{now_time()}] [INFO] parameter '{url.split("?")[1].split("=")[0]}' appears to be vulnerable to SQL injection"
        )
        return

    print(
        f"[{now_time()}] [INFO] parameter '{url.split("?")[1].split("=")[0]}' is not vulnerable to SQL injection"
    )


def buildInjection(url: str, inj: str) -> str:
    chunks = url.split("=")
    return f"{chunks[0]}={inj}"


def read_injections(wordlist_path: str) -> list[str]:
    f = open(wordlist_path, "r")
    return [line.strip() for line in f.readlines()]


def print_ascii():
    print(
        r"""
___________________    ____ ___ .___  _______   ________   ____  ___ 
\_   _____/\_____  \  |    |   \|   | \      \  \_____  \  \   \/  / 
 |    __)_  /  / \  \ |    |   /|   | /   |   \  /   |   \  \     /  
 |        \/   \_/.  \|    |  / |   |/    |    \/    |    \ /     \  
/_______  /\_____\ \_/|______/  |___|\____|__  /\_______  //___/\  \ 
        \/        \__>                       \/         \/       \_/ 
                                                                     
        """
    )


def now_time() -> str:
    return datetime.now().strftime("%H:%M:%S")
