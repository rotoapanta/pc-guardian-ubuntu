"""Zabbix JSON-RPC API client for PC Guardian Ubuntu.

This module provides the client used by the Zabbix provisioning
system to communicate with Zabbix 7 through its JSON-RPC API.

Authentication is performed using an API token for protected methods.

Important:
    Zabbix requires ``apiinfo.version`` to be called without the
    ``Authorization`` header.
"""

from __future__ import annotations

from typing import Any

import requests


class ZabbixAPI:
    """Client for the Zabbix 7 JSON-RPC API."""

    def __init__(
        self,
        url: str,
        token: str,
        verify_tls: bool = True,
        timeout: int = 15,
    ) -> None:
        """Initialize the Zabbix API client.

        Args:
            url: Full URL of the Zabbix API endpoint.
                Example:
                ``http://192.168.1.143/zabbix/api_jsonrpc.php``.
            token: Zabbix API token used for authenticated methods.
            verify_tls: Whether HTTPS certificates should be verified.
            timeout: HTTP request timeout in seconds.
        """
        self.url = url.rstrip("/")
        self.token = token.strip()
        self.verify_tls = verify_tls
        self.timeout = timeout
        self.request_id = 0

    def _next_request_id(self) -> int:
        """Return the next JSON-RPC request identifier."""
        self.request_id += 1
        return self.request_id

    def _headers(self, method: str) -> dict[str, str]:
        """Build the HTTP headers required by a Zabbix API method.

        The ``apiinfo.version`` method must be called without
        authentication.

        Args:
            method: Zabbix API method name.

        Returns:
            Dictionary containing the HTTP headers.

        Raises:
            RuntimeError: If an authenticated method is called without
                a configured API token.
        """
        headers = {
            "Content-Type": "application/json-rpc",
            "Accept": "application/json",
        }

        if method != "apiinfo.version":
            if not self.token:
                raise RuntimeError(f'API token required for Zabbix method "{method}".')

            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def call(
        self,
        method: str,
        params: dict[str, Any] | list[Any] | None = None,
    ) -> Any:
        """Call one Zabbix JSON-RPC API method.

        Args:
            method: Zabbix API method.
                Example: ``hostgroup.get``.
            params: Parameters sent to the method.

        Returns:
            Value returned in the Zabbix ``result`` field.

        Raises:
            RuntimeError: If the connection fails, the response is not
                valid JSON, or Zabbix reports an API error.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params if params is not None else {},
            "id": self._next_request_id(),
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self._headers(method),
                timeout=self.timeout,
                verify=self.verify_tls,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            raise RuntimeError(f"Unable to connect to Zabbix API at {self.url}: {exc}") from exc

        try:
            data = response.json()

        except ValueError as exc:
            raise RuntimeError(
                "Zabbix API returned a non-JSON response. "
                f"HTTP status={response.status_code}. "
                f"Response={response.text[:500]}"
            ) from exc

        if "error" in data:
            error = data["error"]

            code = error.get("code", "unknown")
            message = error.get("message", "Unknown error")
            details = error.get("data", "")

            raise RuntimeError(
                "Zabbix API error | "
                f"method={method} | "
                f"code={code} | "
                f"message={message} | "
                f"details={details}"
            )

        if "result" not in data:
            raise RuntimeError(f'Invalid Zabbix API response for method "{method}": {data}')

        return data["result"]

    def version(self) -> str:
        """Return the Zabbix API version.

        This method intentionally calls ``apiinfo.version`` without
        authentication because Zabbix requires it.
        """
        return str(
            self.call(
                "apiinfo.version",
                {},
            )
        )

    def test_authentication(self) -> bool:
        """Check whether the configured API token is valid.

        A lightweight authenticated request is performed.

        Returns:
            True when authentication succeeds.

        Raises:
            RuntimeError: If the token is invalid or does not have
                permission to query host groups.
        """
        self.call(
            "hostgroup.get",
            {
                "output": ["groupid"],
                "limit": 1,
            },
        )

        return True
