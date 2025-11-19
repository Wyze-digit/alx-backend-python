#!/usr/bin/env python3
"""
Github Org Client module
"""

from typing import Dict
from utils import get_json, memoize


class GithubOrgClient:
    """A Github org client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Init method of GithubOrgClient"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Memoize org - returns organization information"""
        return get_json(self.ORG_URL.format(org=self._org_name))
