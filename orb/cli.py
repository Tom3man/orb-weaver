"""CLI entrypoint for orbweaver-tools."""

from __future__ import annotations

import argparse
import json

from orb import __version__
from orb.common.proxies.test_proxies import test_proxy
from orb.common.user_agents.user_agents import GetUserAgent
from orb.scraper.utils import spoof_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orb", description="Orb Weaver CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="Print package version")
    sub.add_parser("user-agent", help="Print a random user-agent header set")

    spoof = sub.add_parser("spoof-request", help="Send a spoofed GET request")
    spoof.add_argument("url")
    spoof.add_argument("--no-proxy", action="store_true")
    spoof.add_argument("--no-user-agent", action="store_true")

    proxy = sub.add_parser("proxy-test", help="Test a provided proxy")
    proxy.add_argument("http")
    proxy.add_argument("https")

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "user-agent":
        print(json.dumps(GetUserAgent().headers_dict, indent=2))
        return 0

    if args.command == "spoof-request":
        response = spoof_request(
            args.url,
            use_proxies=not args.no_proxy,
            use_user_agent=not args.no_user_agent,
        )
        print(response.status_code)
        return 0

    if args.command == "proxy-test":
        ok = test_proxy({"http": args.http, "https": args.https})
        print("ok" if ok else "fail")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
