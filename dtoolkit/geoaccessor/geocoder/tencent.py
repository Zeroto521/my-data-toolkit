from __future__ import annotations

import hashlib
from functools import partial
from typing import Callable
from urllib.parse import quote_plus
from urllib.parse import urlencode

from geopy.exc import GeocoderAuthenticationFailure
from geopy.exc import GeocoderQueryError
from geopy.exc import GeocoderQuotaExceeded
from geopy.exc import GeocoderServiceError
from geopy.geocoders.base import DEFAULT_SENTINEL
from geopy.geocoders.base import Geocoder
from geopy.location import Location
from geopy.util import logger


__all__ = ("Tencent",)


class Tencent(Geocoder):
    """
    Geocoder using the Tencent Maps API.

    Documentation at:
        https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
    """

    api_path = reverse_path = "/ws/geocoder/v1/"

    def __init__(
        self,
        api_key,
        *,
        scheme: str = None,
        timeout: int = DEFAULT_SENTINEL,
        proxies: dict = DEFAULT_SENTINEL,
        user_agent: str = None,
        ssl_context: ssl.SSLContext = DEFAULT_SENTINEL,
        adapter_factory: Callable = None,
    ):
        """
        :param str api_key: The API key required by Tencent Map to perform
            geocoding requests. API keys are managed through the Tencent APIs
            console (https://lbs.qq.com/dev/console/application/mine).

        :param str scheme:
            See :attr:`geopy.geocoders.options.default_scheme`.

        :param int timeout:
            See :attr:`geopy.geocoders.options.default_timeout`.

        :param dict proxies:
            See :attr:`geopy.geocoders.options.default_proxies`.

        :param str user_agent:
            See :attr:`geopy.geocoders.options.default_user_agent`.

        :type ssl_context: :class:`ssl.SSLContext`
        :param ssl_context:
            See :attr:`geopy.geocoders.options.default_ssl_context`.

        :param callable adapter_factory:
            See :attr:`geopy.geocoders.options.default_adapter_factory`.
        """

        super().__init__(
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
        )
        self.domin = "apis.map.qq.com"
        self.api_key = api_key
        self.api = f"{self.scheme}://{self.domin}{self.api_path}"
        self.reverse_api = f"{self.scheme}://{self.domin}{self.reverse_path}"

    def geocode(
        self,
        query: str,
        *,
        region: str = None,
        exactly_one: bool = True,
        timeout: int = DEFAULT_SENTINEL,
    ) -> None | Location | list[Location]:
        """
        Return a location point by address.

        :param str query: The address or query you wish to geocode.

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geopy.location.Location` or a list of them, if
            ``exactly_one=False``.
        """

        params = {
            "address": query,
            **({"region": region} if region else {}),
            "key": self.api_key,
        }
        url = self._construct_url(self.api, params)

        logger.debug(f"{self.__class__.__name__}.geocode: {url}")
        callback = partial(self._parse_json, exactly_one=exactly_one, address="title")

        return self._call_geocoder(url, callback, timeout=timeout)

    def reverse(
        self,
        query: str,
        *,
        exactly_one: bool = True,
        timeout: int = DEFAULT_SENTINEL,
    ) -> None | Location | list[Location]:
        """
        Return an address by location point.

        :type query: :class:`geopy.point.Point`, list or tuple of ``(latitude,
            longitude)``, or string as ``"%(latitude)s, %(longitude)s"``.
        :param query: The coordinates for which you wish to obtain the
            closest human-readable addresses.

        :param bool exactly_one: Return one result or a list of results, if
            available. Tencent's API always return at most one result.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geopy.location.Location` or a list of them, if
            ``exactly_one=False``.
        """

        params = {
            "location": self._coerce_point_to_string(query),
            "key": self.api_key,
        }
        url = self._construct_url(self.reverse_api, params)

        logger.debug(f"{self.__class__.__name__}.reverse: {url}")
        callback = partial(self._parse_json, exactly_one=exactly_one)

        return self._call_geocoder(url, callback, timeout=timeout)

    def _construct_url(self, base_api: str, params: dict) -> str:
        """
        Construct geocoding request url.

        :param str base_api: Geocoding function base address - self.api
            or self.reverse_api.

        :param dict params: Geocoding params.

        :return: string URL.
        """

        return "?".join((base_api, urlencode(params)))

    def _parse_json(
        self,
        response: dict,
        exactly_one: bool = True,
        status: str = "status",
        address: str = "address",
        location: str = "location",
        lat: str = "lat",
        lng: str = "lng",
    ) -> None | Location | list[Location]:
        """
        Returns location, (latitude, longitude) from JSON feed.
        """

        self._check_status(response.get(status))
        if response is None or "result" not in response:
            return

        place = self._parse_place(
            response["result"],
            location=location,
            address=address,
            lat=lat,
            lng=lng,
        )
        return place if exactly_one else [place]

    def _parse_place(
        self,
        place: dict,
        address: str = "address",
        location: str = "location",
        lat: str = "lat",
        lng: str = "lng",
    ) -> None | Location:
        """
        Get the location, lat, and lng from a single JSON place.
        """

        if place is None or address not in place or location not in place:
            return

        return Location(
            place[address],
            self._parse_coordinate(
                place[location],
                lat=lat,
                lng=lng,
            ),
            place,
        )

    def _parse_coordinate(
        self,
        location: dict,
        lat: str = "lat",
        lng: str = "lng",
    ) -> tuple(float | None, float | None):
        """
        Get the lat and lng from a single JSON location.
        """

        if location is None or lat not in location or lng not in location:
            return (None, None)

        return (location[lat], location[lng])

    def _check_status(self, status: str | int):
        """
        Validates error statuses.
        """

        if status == 0:
            # When there are no results, just return.
            return
        if status == 1:
            raise GeocoderServiceError("Internal server error.")
        elif status == 2:
            raise GeocoderQueryError("Invalid request.")
        elif status == 3:
            raise GeocoderAuthenticationFailure("Authentication failure.")
        elif status == 4:
            raise GeocoderQuotaExceeded("Quota validate failure.")
        elif status == 5:
            raise GeocoderQueryError("AK Illegal or Not Exist.")
        elif status == 101:
            raise GeocoderAuthenticationFailure("No AK")
        elif status == 102:
            raise GeocoderAuthenticationFailure("MCODE Error")
        elif status == 200:
            raise GeocoderAuthenticationFailure("Invalid AK")
        elif status == 211:
            raise GeocoderAuthenticationFailure("Invalid SN")
        elif 200 <= status < 300:
            raise GeocoderAuthenticationFailure("Authentication Failure")
        elif 300 <= status < 500:
            raise GeocoderQuotaExceeded("Quota Error.")
        else:
            raise GeocoderQueryError("Unknown error. Status: %r" % status)
