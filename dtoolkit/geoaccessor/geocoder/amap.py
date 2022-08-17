from __future__ import annotations

from functools import partial
from typing import Callable

from geopy.exc import GeocoderAuthenticationFailure
from geopy.exc import GeocoderQueryError
from geopy.exc import GeocoderQuotaExceeded
from geopy.exc import GeocoderServiceError
from geopy.exc import GeocoderTimedOut
from geopy.geocoders.base import DEFAULT_SENTINEL
from geopy.geocoders.base import Geocoder
from geopy.location import Location
from geopy.util import logger


__all__ = ("Amap",)


class Amap(Geocoder):
    """
    Geocoder using the Amap Maps API.

    Documentation at:
        https://lbs.amap.com/api/webservice/guide/api/georegeo
    """

    api_path = "/v3/geocode/geo/"
    reverse_path = "/v3/geocode/regeo/"

    def __init__(
        self,
        api_key: str,
        *,
        sig: str = None,
        scheme: str = None,
        timeout: int = DEFAULT_SENTINEL,
        proxies: dict = DEFAULT_SENTINEL,
        user_agent: str = None,
        ssl_context: ssl.SSLContext = DEFAULT_SENTINEL,
        adapter_factory: Callable = None,
    ):
        """
        :param str api_key: The API key required by Amap Map to perform
            geocoding requests. API keys are managed through the Amap APIs
            console (https://console.amap.com/dev/key/app).

        :param str sig: The digital signature (sig) to calculate the SN
            parameter in request if authentication setting requires
            (https://lbs.amap.com/faq/quota-key/key/41169).

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
        self.api_key = api_key
        self.sig = sig
        self.domin = "restapi.amap.com"
        self.api = f"{self.scheme}://{self.domin}{self.api_path}"
        self.reverse_api = f"{self.scheme}://{self.domin}{self.reverse_path}"

    def geocode(
        self,
        query: str,
        *,
        city: str = None,
        exactly_one: bool = True,
        timeout: int = DEFAULT_SENTINEL,
    ) -> None | Location | list[Location]:
        """
        Return a location point by address.

        :param str query: The address or query you wish to geocode.

        :param str city: The city of address.

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
            "city": city,
            "key": self.api_key,
        }
        url = self._construct_url(self.api, params)

        logger.debug(f"{self.__class__.__name__}.geocode: {url}")
        callback = partial(
            self._parse_json,
            exactly_one=exactly_one,
            result="geocodes",
        )

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
        callback = partial(
            self._parse_json,
            exactly_one=exactly_one,
            result="regeocode",
        )

        return self._call_geocoder(url, callback, timeout=timeout)

    def _construct_url(self, base_api: str, params: dict) -> str:
        """
        Construct geocoding request url.

        :param str base_api: Geocoding function base address - self.api
            or self.reverse_api.

        :param dict params: Geocoding params.

        :return: string URL.
        """
        from urllib.parse import urlencode

        # Remove empty value item
        params = {k: v for k, v in params.items() if v}
        return "?".join((base_api, urlencode(params)))

    def _parse_json(
        self,
        response: dict,
        exactly_one: bool = True,
        result: str = "result",
        code: str = "infocode",
        info: str = "info",
        address: str = "formatted_address",
        location: str = "location",
    ) -> None | Location | list[Location]:
        """
        Returns location, (latitude, longitude) from JSON feed.
        """

        self._check_status(response.get(code), response.get(info))
        if response is None or result not in response:
            return

        place = self._parse_place(
            response["result"],
            location=location,
            address=address,
        )
        return place if exactly_one else [place]

    def _parse_place(
        self,
        place: dict,
        address: str = "formatted_address",
        location: str = "location",
    ) -> None | Location:
        """
        Get the location, lat, and lng from a single JSON place.
        """

        if place is None or address not in place or location not in place:
            return

        return Location(
            place[address],
            self._parse_coordinate(place[location]),
            place,
        )

    def _parse_coordinate(self, location: str) -> tuple(float | None, float | None):
        """
        Get the lat and lng from a string ("lat,lng").
        """

        if location is None:
            return (None, None)

        return tuple(map(float, location.split(",")))

    def _check_status(self, code: int, info: str):
        """
        Validates error statuses.

        Documentation at:
            https://lbs.amap.com/api/webservice/guide/tools/info
        """

        if code == 10000:
            return
        elif code in {
            10001,
            10002,
            10005,
            10006,
            10007,
            10009,
            10010,
            10012,
            10026,
            10041,
        }:
            raise GeocoderAuthenticationFailure(f"{info}.")
        elif (
            code
            in {
                10003,
                10004,
                10014,
                10015,
                10019,
                10020,
                10021,
                10029,
                10044,
                10045,
            }
            or 40000 <= code <= 50000
        ):
            raise GeocoderQuotaExceeded(f"{info}.")
        elif code in {10013, 10017} or 20000 <= code < 30000:
            raise GeocoderQueryError(f"{info}.")
        elif code == 10011 or 30000 <= code < 40000:
            raise GeocoderServiceError(f"{info}.")
        else:
            raise GeocoderQueryError(f"{info}.")
