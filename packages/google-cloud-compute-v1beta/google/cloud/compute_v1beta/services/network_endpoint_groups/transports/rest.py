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
from .rest_base import _BaseNetworkEndpointGroupsRestTransport

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


class NetworkEndpointGroupsRestInterceptor:
    """Interceptor for NetworkEndpointGroups.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the NetworkEndpointGroupsRestTransport.

    .. code-block:: python
        class MyCustomNetworkEndpointGroupsInterceptor(NetworkEndpointGroupsRestInterceptor):
            def pre_aggregated_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_aggregated_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_attach_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_attach_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_detach_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detach_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_insert(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_insert(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_network_endpoints(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_network_endpoints(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = NetworkEndpointGroupsRestTransport(interceptor=MyCustomNetworkEndpointGroupsInterceptor())
        client = NetworkEndpointGroupsClient(transport=transport)


    """

    def pre_aggregated_list(
        self,
        request: compute.AggregatedListNetworkEndpointGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.AggregatedListNetworkEndpointGroupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for aggregated_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_aggregated_list(
        self, response: compute.NetworkEndpointGroupAggregatedList
    ) -> compute.NetworkEndpointGroupAggregatedList:
        """Post-rpc interceptor for aggregated_list

        DEPRECATED. Please use the `post_aggregated_list_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_aggregated_list` interceptor runs
        before the `post_aggregated_list_with_metadata` interceptor.
        """
        return response

    def post_aggregated_list_with_metadata(
        self,
        response: compute.NetworkEndpointGroupAggregatedList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.NetworkEndpointGroupAggregatedList,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for aggregated_list

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_aggregated_list_with_metadata`
        interceptor in new development instead of the `post_aggregated_list` interceptor.
        When both interceptors are used, this `post_aggregated_list_with_metadata` interceptor runs after the
        `post_aggregated_list` interceptor. The (possibly modified) response returned by
        `post_aggregated_list` will be passed to
        `post_aggregated_list_with_metadata`.
        """
        return response, metadata

    def pre_attach_network_endpoints(
        self,
        request: compute.AttachNetworkEndpointsNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.AttachNetworkEndpointsNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for attach_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_attach_network_endpoints(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for attach_network_endpoints

        DEPRECATED. Please use the `post_attach_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_attach_network_endpoints` interceptor runs
        before the `post_attach_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_attach_network_endpoints_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for attach_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_attach_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_attach_network_endpoints` interceptor.
        When both interceptors are used, this `post_attach_network_endpoints_with_metadata` interceptor runs after the
        `post_attach_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_attach_network_endpoints` will be passed to
        `post_attach_network_endpoints_with_metadata`.
        """
        return response, metadata

    def pre_delete(
        self,
        request: compute.DeleteNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.DeleteNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for delete

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_delete(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for delete

        DEPRECATED. Please use the `post_delete_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_delete` interceptor runs
        before the `post_delete_with_metadata` interceptor.
        """
        return response

    def post_delete_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for delete

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_delete_with_metadata`
        interceptor in new development instead of the `post_delete` interceptor.
        When both interceptors are used, this `post_delete_with_metadata` interceptor runs after the
        `post_delete` interceptor. The (possibly modified) response returned by
        `post_delete` will be passed to
        `post_delete_with_metadata`.
        """
        return response, metadata

    def pre_detach_network_endpoints(
        self,
        request: compute.DetachNetworkEndpointsNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.DetachNetworkEndpointsNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for detach_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_detach_network_endpoints(
        self, response: compute.Operation
    ) -> compute.Operation:
        """Post-rpc interceptor for detach_network_endpoints

        DEPRECATED. Please use the `post_detach_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_detach_network_endpoints` interceptor runs
        before the `post_detach_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_detach_network_endpoints_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for detach_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_detach_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_detach_network_endpoints` interceptor.
        When both interceptors are used, this `post_detach_network_endpoints_with_metadata` interceptor runs after the
        `post_detach_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_detach_network_endpoints` will be passed to
        `post_detach_network_endpoints_with_metadata`.
        """
        return response, metadata

    def pre_get(
        self,
        request: compute.GetNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.GetNetworkEndpointGroupRequest, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Pre-rpc interceptor for get

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_get(
        self, response: compute.NetworkEndpointGroup
    ) -> compute.NetworkEndpointGroup:
        """Post-rpc interceptor for get

        DEPRECATED. Please use the `post_get_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_get` interceptor runs
        before the `post_get_with_metadata` interceptor.
        """
        return response

    def post_get_with_metadata(
        self,
        response: compute.NetworkEndpointGroup,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.NetworkEndpointGroup, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for get

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_get_with_metadata`
        interceptor in new development instead of the `post_get` interceptor.
        When both interceptors are used, this `post_get_with_metadata` interceptor runs after the
        `post_get` interceptor. The (possibly modified) response returned by
        `post_get` will be passed to
        `post_get_with_metadata`.
        """
        return response, metadata

    def pre_insert(
        self,
        request: compute.InsertNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.InsertNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for insert

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_insert(self, response: compute.Operation) -> compute.Operation:
        """Post-rpc interceptor for insert

        DEPRECATED. Please use the `post_insert_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_insert` interceptor runs
        before the `post_insert_with_metadata` interceptor.
        """
        return response

    def post_insert_with_metadata(
        self,
        response: compute.Operation,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[compute.Operation, Sequence[Tuple[str, Union[str, bytes]]]]:
        """Post-rpc interceptor for insert

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_insert_with_metadata`
        interceptor in new development instead of the `post_insert` interceptor.
        When both interceptors are used, this `post_insert_with_metadata` interceptor runs after the
        `post_insert` interceptor. The (possibly modified) response returned by
        `post_insert` will be passed to
        `post_insert_with_metadata`.
        """
        return response, metadata

    def pre_list(
        self,
        request: compute.ListNetworkEndpointGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ListNetworkEndpointGroupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_list(
        self, response: compute.NetworkEndpointGroupList
    ) -> compute.NetworkEndpointGroupList:
        """Post-rpc interceptor for list

        DEPRECATED. Please use the `post_list_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_list` interceptor runs
        before the `post_list_with_metadata` interceptor.
        """
        return response

    def post_list_with_metadata(
        self,
        response: compute.NetworkEndpointGroupList,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.NetworkEndpointGroupList, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for list

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_list_with_metadata`
        interceptor in new development instead of the `post_list` interceptor.
        When both interceptors are used, this `post_list_with_metadata` interceptor runs after the
        `post_list` interceptor. The (possibly modified) response returned by
        `post_list` will be passed to
        `post_list_with_metadata`.
        """
        return response, metadata

    def pre_list_network_endpoints(
        self,
        request: compute.ListNetworkEndpointsNetworkEndpointGroupsRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.ListNetworkEndpointsNetworkEndpointGroupsRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for list_network_endpoints

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_list_network_endpoints(
        self, response: compute.NetworkEndpointGroupsListNetworkEndpoints
    ) -> compute.NetworkEndpointGroupsListNetworkEndpoints:
        """Post-rpc interceptor for list_network_endpoints

        DEPRECATED. Please use the `post_list_network_endpoints_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_list_network_endpoints` interceptor runs
        before the `post_list_network_endpoints_with_metadata` interceptor.
        """
        return response

    def post_list_network_endpoints_with_metadata(
        self,
        response: compute.NetworkEndpointGroupsListNetworkEndpoints,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.NetworkEndpointGroupsListNetworkEndpoints,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for list_network_endpoints

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_list_network_endpoints_with_metadata`
        interceptor in new development instead of the `post_list_network_endpoints` interceptor.
        When both interceptors are used, this `post_list_network_endpoints_with_metadata` interceptor runs after the
        `post_list_network_endpoints` interceptor. The (possibly modified) response returned by
        `post_list_network_endpoints` will be passed to
        `post_list_network_endpoints_with_metadata`.
        """
        return response, metadata

    def pre_test_iam_permissions(
        self,
        request: compute.TestIamPermissionsNetworkEndpointGroupRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.TestIamPermissionsNetworkEndpointGroupRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the NetworkEndpointGroups server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: compute.TestPermissionsResponse
    ) -> compute.TestPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        DEPRECATED. Please use the `post_test_iam_permissions_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the NetworkEndpointGroups server but before
        it is returned to user code. This `post_test_iam_permissions` interceptor runs
        before the `post_test_iam_permissions_with_metadata` interceptor.
        """
        return response

    def post_test_iam_permissions_with_metadata(
        self,
        response: compute.TestPermissionsResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        compute.TestPermissionsResponse, Sequence[Tuple[str, Union[str, bytes]]]
    ]:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the NetworkEndpointGroups server but before it is returned to user code.

        We recommend only using this `post_test_iam_permissions_with_metadata`
        interceptor in new development instead of the `post_test_iam_permissions` interceptor.
        When both interceptors are used, this `post_test_iam_permissions_with_metadata` interceptor runs after the
        `post_test_iam_permissions` interceptor. The (possibly modified) response returned by
        `post_test_iam_permissions` will be passed to
        `post_test_iam_permissions_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class NetworkEndpointGroupsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: NetworkEndpointGroupsRestInterceptor


class NetworkEndpointGroupsRestTransport(_BaseNetworkEndpointGroupsRestTransport):
    """REST backend synchronous transport for NetworkEndpointGroups.

    The NetworkEndpointGroups API.

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
        interceptor: Optional[NetworkEndpointGroupsRestInterceptor] = None,
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
        self._interceptor = interceptor or NetworkEndpointGroupsRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AggregatedList(
        _BaseNetworkEndpointGroupsRestTransport._BaseAggregatedList,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.AggregatedList")

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
            request: compute.AggregatedListNetworkEndpointGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroupAggregatedList:
            r"""Call the aggregated list method over HTTP.

            Args:
                request (~.compute.AggregatedListNetworkEndpointGroupsRequest):
                    The request object. A request message for
                NetworkEndpointGroups.AggregatedList.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroupAggregatedList:

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseAggregatedList._get_http_options()
            )

            request, metadata = self._interceptor.pre_aggregated_list(request, metadata)
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseAggregatedList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseAggregatedList._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.AggregatedList",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "AggregatedList",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._AggregatedList._get_response(
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
            resp = compute.NetworkEndpointGroupAggregatedList()
            pb_resp = compute.NetworkEndpointGroupAggregatedList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_aggregated_list(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_aggregated_list_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        compute.NetworkEndpointGroupAggregatedList.to_json(response)
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.aggregated_list",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "AggregatedList",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _AttachNetworkEndpoints(
        _BaseNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.AttachNetworkEndpoints")

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
                data=body,
            )
            return response

        def __call__(
            self,
            request: compute.AttachNetworkEndpointsNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the attach network endpoints method over HTTP.

            Args:
                request (~.compute.AttachNetworkEndpointsNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.AttachNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_attach_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseAttachNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.AttachNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "AttachNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._AttachNetworkEndpoints._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_attach_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_attach_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.attach_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "AttachNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Delete(
        _BaseNetworkEndpointGroupsRestTransport._BaseDelete,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.Delete")

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
            request: compute.DeleteNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the delete method over HTTP.

            Args:
                request (~.compute.DeleteNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.Delete. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseDelete._get_http_options()
            )

            request, metadata = self._interceptor.pre_delete(request, metadata)
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseDelete._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseDelete._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.Delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Delete",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._Delete._get_response(
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
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_delete(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_delete_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.delete",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Delete",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _DetachNetworkEndpoints(
        _BaseNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.DetachNetworkEndpoints")

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
                data=body,
            )
            return response

        def __call__(
            self,
            request: compute.DetachNetworkEndpointsNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the detach network endpoints method over HTTP.

            Args:
                request (~.compute.DetachNetworkEndpointsNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.DetachNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_detach_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseDetachNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.DetachNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "DetachNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._DetachNetworkEndpoints._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_detach_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_detach_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.detach_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "DetachNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Get(
        _BaseNetworkEndpointGroupsRestTransport._BaseGet, NetworkEndpointGroupsRestStub
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.Get")

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
            request: compute.GetNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroup:
            r"""Call the get method over HTTP.

            Args:
                request (~.compute.GetNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.Get. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroup:
                    Represents a collection of network
                endpoints. A network endpoint group
                (NEG) defines how a set of endpoints
                should be reached, whether they are
                reachable, and where they are located.
                For more information about using NEGs
                for different use cases, see Network
                endpoint groups overview.

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseGet._get_http_options()
            )

            request, metadata = self._interceptor.pre_get(request, metadata)
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseGet._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseNetworkEndpointGroupsRestTransport._BaseGet._get_query_params_json(
                    transcoded_request
                )
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.Get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Get",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._Get._get_response(
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
            resp = compute.NetworkEndpointGroup()
            pb_resp = compute.NetworkEndpointGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_get(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_get_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.NetworkEndpointGroup.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.get",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Get",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _Insert(
        _BaseNetworkEndpointGroupsRestTransport._BaseInsert,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.Insert")

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
                data=body,
            )
            return response

        def __call__(
            self,
            request: compute.InsertNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.Operation:
            r"""Call the insert method over HTTP.

            Args:
                request (~.compute.InsertNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.Insert. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.Operation:
                    Represents an Operation resource. Google Compute Engine
                has three Operation resources: \*
                `Global </compute/docs/reference/rest/beta/globalOperations>`__
                \*
                `Regional </compute/docs/reference/rest/beta/regionOperations>`__
                \*
                `Zonal </compute/docs/reference/rest/beta/zoneOperations>`__
                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses. Operations can be global, regional or zonal.
                - For global operations, use the ``globalOperations``
                resource. - For regional operations, use the
                ``regionOperations`` resource. - For zonal operations,
                use the ``zoneOperations`` resource. For more
                information, read Global, Regional, and Zonal Resources.
                Note that completed Operation resources have a limited
                retention period.

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseInsert._get_http_options()
            )

            request, metadata = self._interceptor.pre_insert(request, metadata)
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseInsert._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetworkEndpointGroupsRestTransport._BaseInsert._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseInsert._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.Insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Insert",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._Insert._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.Operation()
            pb_resp = compute.Operation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_insert(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_insert_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.Operation.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.insert",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "Insert",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _List(
        _BaseNetworkEndpointGroupsRestTransport._BaseList, NetworkEndpointGroupsRestStub
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.List")

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
            request: compute.ListNetworkEndpointGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroupList:
            r"""Call the list method over HTTP.

            Args:
                request (~.compute.ListNetworkEndpointGroupsRequest):
                    The request object. A request message for
                NetworkEndpointGroups.List. See the
                method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroupList:

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseList._get_http_options()
            )

            request, metadata = self._interceptor.pre_list(request, metadata)
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseList._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseList._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.List",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "List",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = NetworkEndpointGroupsRestTransport._List._get_response(
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
            resp = compute.NetworkEndpointGroupList()
            pb_resp = compute.NetworkEndpointGroupList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_with_metadata(resp, response_metadata)
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.NetworkEndpointGroupList.to_json(
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
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.list",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "List",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _ListNetworkEndpoints(
        _BaseNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.ListNetworkEndpoints")

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
                data=body,
            )
            return response

        def __call__(
            self,
            request: compute.ListNetworkEndpointsNetworkEndpointGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.NetworkEndpointGroupsListNetworkEndpoints:
            r"""Call the list network endpoints method over HTTP.

            Args:
                request (~.compute.ListNetworkEndpointsNetworkEndpointGroupsRequest):
                    The request object. A request message for
                NetworkEndpointGroups.ListNetworkEndpoints.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.NetworkEndpointGroupsListNetworkEndpoints:

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_http_options()
            )

            request, metadata = self._interceptor.pre_list_network_endpoints(
                request, metadata
            )
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseListNetworkEndpoints._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.ListNetworkEndpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "ListNetworkEndpoints",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                NetworkEndpointGroupsRestTransport._ListNetworkEndpoints._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.NetworkEndpointGroupsListNetworkEndpoints()
            pb_resp = compute.NetworkEndpointGroupsListNetworkEndpoints.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_list_network_endpoints(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_list_network_endpoints_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = (
                        compute.NetworkEndpointGroupsListNetworkEndpoints.to_json(
                            response
                        )
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.list_network_endpoints",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "ListNetworkEndpoints",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _TestIamPermissions(
        _BaseNetworkEndpointGroupsRestTransport._BaseTestIamPermissions,
        NetworkEndpointGroupsRestStub,
    ):
        def __hash__(self):
            return hash("NetworkEndpointGroupsRestTransport.TestIamPermissions")

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
                data=body,
            )
            return response

        def __call__(
            self,
            request: compute.TestIamPermissionsNetworkEndpointGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> compute.TestPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.compute.TestIamPermissionsNetworkEndpointGroupRequest):
                    The request object. A request message for
                NetworkEndpointGroups.TestIamPermissions.
                See the method description for details.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                    sent along with the request as metadata. Normally, each value must be of type `str`,
                    but for metadata keys ending with the suffix `-bin`, the corresponding values must
                    be of type `bytes`.

            Returns:
                ~.compute.TestPermissionsResponse:

            """

            http_options = (
                _BaseNetworkEndpointGroupsRestTransport._BaseTestIamPermissions._get_http_options()
            )

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseNetworkEndpointGroupsRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseNetworkEndpointGroupsRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseNetworkEndpointGroupsRestTransport._BaseTestIamPermissions._get_query_params_json(
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
                    f"Sending request for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.TestIamPermissions",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "TestIamPermissions",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = (
                NetworkEndpointGroupsRestTransport._TestIamPermissions._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                    body,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = compute.TestPermissionsResponse()
            pb_resp = compute.TestPermissionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)

            resp = self._interceptor.post_test_iam_permissions(resp)
            response_metadata = [(k, str(v)) for k, v in response.headers.items()]
            resp, _ = self._interceptor.post_test_iam_permissions_with_metadata(
                resp, response_metadata
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = compute.TestPermissionsResponse.to_json(response)
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.cloud.compute_v1beta.NetworkEndpointGroupsClient.test_iam_permissions",
                    extra={
                        "serviceName": "google.cloud.compute.v1beta.NetworkEndpointGroups",
                        "rpcName": "TestIamPermissions",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListNetworkEndpointGroupsRequest],
        compute.NetworkEndpointGroupAggregatedList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AggregatedList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def attach_network_endpoints(
        self,
    ) -> Callable[
        [compute.AttachNetworkEndpointsNetworkEndpointGroupRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AttachNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete(
        self,
    ) -> Callable[[compute.DeleteNetworkEndpointGroupRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Delete(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def detach_network_endpoints(
        self,
    ) -> Callable[
        [compute.DetachNetworkEndpointsNetworkEndpointGroupRequest], compute.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DetachNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetNetworkEndpointGroupRequest], compute.NetworkEndpointGroup
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Get(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def insert(
        self,
    ) -> Callable[[compute.InsertNetworkEndpointGroupRequest], compute.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Insert(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListNetworkEndpointGroupsRequest], compute.NetworkEndpointGroupList
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._List(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_network_endpoints(
        self,
    ) -> Callable[
        [compute.ListNetworkEndpointsNetworkEndpointGroupsRequest],
        compute.NetworkEndpointGroupsListNetworkEndpoints,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworkEndpoints(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsNetworkEndpointGroupRequest],
        compute.TestPermissionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("NetworkEndpointGroupsRestTransport",)
