# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import dataclasses
import json  # type: ignore
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
import google.protobuf
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.compute_v1beta.types import compute

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseInterconnectRemoteLocationsRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class InterconnectRemoteLocationsRestInterceptor:
    """Interceptor for InterconnectRemoteLocations.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the InterconnectRemoteLocationsRestTransport.

    .. code-block:: python
        class MyCustomInterconnectRemoteLocationsInterceptor(InterconnectRemoteLocationsRestInterceptor):
            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = InterconnectRemoteLocationsRestTransport(interceptor=MyCustomInterconnectRemoteLocationsInterceptor())
        client = InterconnectRemoteLocationsClient(transport=transport)


    """

    def pre_get(
        self,
        request: compute.GetInterconnectRemoteLocationRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.GetInterconnectRemoteLocationRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InterconnectRemoteLocations server.
        """
        return request, metadata

    def post_get(
        self, response: compute.InterconnectRemoteLocation
    ) -> compute.InterconnectRemoteLocation:
        """Post-rpc interceptor for get

        DEPRECATED. Please use the `post_get_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the InterconnectRemoteLocations server but before
        it is returned to user code. This `post_get` interceptor runs
        before the `post_get_with_metadata` interceptor.
        """
        return response

    def post_get_with_metadata(
        self,
        response: compute.InterconnectRemoteLocation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.InterconnectRemoteLocation, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for get

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the InterconnectRemoteLocations server but before it is returned to user code.

        We recommend only using this `post_get_with_metadata`
        interceptor in new development instead of the `post_get` interceptor.
        When both interceptors are used, this `post_get_with_metadata` interceptor runs after the
        `post_get` interceptor. The (possibly modified) response returned by
        `post_get` will be passed to
        `post_get_with_metadata`.
        """
        return response, metadata

    def pre_list(
        self,
        request: compute.ListInterconnectRemoteLocationsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ListInterconnectRemoteLocationsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the InterconnectRemoteLocations server.
        """
        return request, metadata

    def post_list(
        self, response: compute.InterconnectRemoteLocationList
    ) -> compute.InterconnectRemoteLocationList:
        """Post-rpc interceptor for list

        DEPRECATED. Please use the `post_list_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the InterconnectRemoteLocations server but before
        it is returned to user code. This `post_list` interceptor runs
        before the `post_list_with_metadata` interceptor.
        """
        return response

    def post_list_with_metadata(
        self,
        response: compute.InterconnectRemoteLocationList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.InterconnectRemoteLocationList, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the InterconnectRemoteLocations server but before it is returned to user code.

        We recommend only using this `post_list_with_metadata`
        interceptor in new development instead of the `post_list` interceptor.
        When both interceptors are used, this `post_list_with_metadata` interceptor runs after the
        `post_list` interceptor. The (possibly modified) response returned by
        `post_list` will be passed to
        `post_list_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class InterconnectRemoteLocationsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: InterconnectRemoteLocationsRestInterceptor


class InterconnectRemoteLocationsRestTransport(
    _BaseInterconnectRemoteLocationsRestTransport
):
    """REST backend synchronous transport for InterconnectRemoteLocations.

    The InterconnectRemoteLocations API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[InterconnectRemoteLocationsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'compute.googleapis.com').
             credentials (Optional[google.auth.credentials.Credentials]): The
                 authorization credentials to attach to requests. These
                 credentials identify the application to the service; if none
                 are specified, the client will attempt to ascertain the
                 credentials from the environment.

             credentials_file (Optional[str]): A file with credentials that can
                 be loaded with :func:`google.auth.load_credentials_from_file`.
                 This argument is ignored if ``channel`` is provided.
             scopes (Optional(Sequence[str])): A list of scopes. This argument is
                 ignored if ``channel`` is provided.
             client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                 certificate to configure mutual TLS HTTP channel. It is ignored
                 if ``channel`` is provided.
             quota_project_id (Optional[str]): An optional project to use for billing
                 and quota.
             client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                 The client info used to send a user-agent string along with
                 API requests. If ``None``, then default info will be used.
                 Generally, you only need to set this if you are developing
                 your own client library.
             always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                 be used for service account credentials.
             url_scheme: the protocol scheme for the API endpoint.  Normally
                 "https", but for testing or local servers,
                 "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or InterconnectRemoteLocationsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _Get(
        _BaseInterconnectRemoteLocationsRestTransport._BaseGet,
        InterconnectRemoteLocationsRestStub,
    ):
        def __hash__(self):
            return hash("InterconnectRemoteLocationsRestTransport.Get")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: compute.GetInterconnectRemoteLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.InterconnectRemoteLocation:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetInterconnectRemoteLocationRequest):
                    The request object. A request message for
                InterconnectRemoteLocations.Get. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.InterconnectRemoteLocation:
                    Represents a Cross-Cloud Interconnect
                Remote Location resource. You can use
                this resource to find remote location
                details about an Interconnect attachment
                (VLAN).

            """

            http_options = (
                _BaseInterconnectRemoteLocationsRestTransport._BaseGet._get_http_options()
            )

            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseInterconnectRemoteLocationsRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInterconnectRemoteLocationsRestTransport._BaseGet._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.compute_v1beta.InterconnectRemoteLocationsClient.Get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.InterconnectRemoteLocations",
                        "rpcName": "Get",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = InterconnectRemoteLocationsRestTransport._Get._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InterconnectRemoteLocation()
            pb_resp = compute.InterconnectRemoteLocation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.InterconnectRemoteLocation.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.InterconnectRemoteLocationsClient.get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.InterconnectRemoteLocations",
                        "rpcName": "Get",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _List(
        _BaseInterconnectRemoteLocationsRestTransport._BaseList,
        InterconnectRemoteLocationsRestStub,
    ):
        def __hash__(self):
            return hash("InterconnectRemoteLocationsRestTransport.List")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: compute.ListInterconnectRemoteLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.InterconnectRemoteLocationList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListInterconnectRemoteLocationsRequest):
                    The request object. A request message for
                InterconnectRemoteLocations.List. See
                the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.InterconnectRemoteLocationList:
                    Response to the list request, and
                contains a list of interconnect remote
                locations.

            """

            http_options = (
                _BaseInterconnectRemoteLocationsRestTransport._BaseList._get_http_options()
            )

            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseInterconnectRemoteLocationsRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseInterconnectRemoteLocationsRestTransport._BaseList._get_query_params_json(
                transcoded_request
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.cloud.compute_v1beta.InterconnectRemoteLocationsClient.List",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.InterconnectRemoteLocations",
                        "rpcName": "List",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = InterconnectRemoteLocationsRestTransport._List._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.InterconnectRemoteLocationList()
            pb_resp = compute.InterconnectRemoteLocationList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.InterconnectRemoteLocationList.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.InterconnectRemoteLocationsClient.list",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.InterconnectRemoteLocations",
                        "rpcName": "List",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetInterconnectRemoteLocationRequest],
        compute.InterconnectRemoteLocation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListInterconnectRemoteLocationsRequest],
        compute.InterconnectRemoteLocationList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("InterconnectRemoteLocationsRestTransport",)
