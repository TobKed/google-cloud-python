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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.dataplex_v1.types import analyze, resources, service, tasks

from .base import DEFAULT_CLIENT_INFO, DataplexServiceTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.dataplex.v1.DataplexService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.dataplex.v1.DataplexService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class DataplexServiceGrpcTransport(DataplexServiceTransport):
    """gRPC backend transport for DataplexService.

    Dataplex service provides data lakes as a service. The
    primary resources offered by this service are Lakes, Zones and
    Assets which collectively allow a data administrator to
    organize, manage, secure and catalog data across their
    organization located across cloud projects in a variety of
    storage systems including Cloud Storage and BigQuery.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "dataplex.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dataplex.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "dataplex.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self._logged_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_lake(
        self,
    ) -> Callable[[service.CreateLakeRequest], operations_pb2.Operation]:
        r"""Return a callable for the create lake method over gRPC.

        Creates a lake resource.

        Returns:
            Callable[[~.CreateLakeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_lake" not in self._stubs:
            self._stubs["create_lake"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CreateLake",
                request_serializer=service.CreateLakeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_lake"]

    @property
    def update_lake(
        self,
    ) -> Callable[[service.UpdateLakeRequest], operations_pb2.Operation]:
        r"""Return a callable for the update lake method over gRPC.

        Updates a lake resource.

        Returns:
            Callable[[~.UpdateLakeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_lake" not in self._stubs:
            self._stubs["update_lake"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/UpdateLake",
                request_serializer=service.UpdateLakeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_lake"]

    @property
    def delete_lake(
        self,
    ) -> Callable[[service.DeleteLakeRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete lake method over gRPC.

        Deletes a lake resource. All zones within the lake
        must be deleted before the lake can be deleted.

        Returns:
            Callable[[~.DeleteLakeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_lake" not in self._stubs:
            self._stubs["delete_lake"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/DeleteLake",
                request_serializer=service.DeleteLakeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_lake"]

    @property
    def list_lakes(
        self,
    ) -> Callable[[service.ListLakesRequest], service.ListLakesResponse]:
        r"""Return a callable for the list lakes method over gRPC.

        Lists lake resources in a project and location.

        Returns:
            Callable[[~.ListLakesRequest],
                    ~.ListLakesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_lakes" not in self._stubs:
            self._stubs["list_lakes"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListLakes",
                request_serializer=service.ListLakesRequest.serialize,
                response_deserializer=service.ListLakesResponse.deserialize,
            )
        return self._stubs["list_lakes"]

    @property
    def get_lake(self) -> Callable[[service.GetLakeRequest], resources.Lake]:
        r"""Return a callable for the get lake method over gRPC.

        Retrieves a lake resource.

        Returns:
            Callable[[~.GetLakeRequest],
                    ~.Lake]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_lake" not in self._stubs:
            self._stubs["get_lake"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetLake",
                request_serializer=service.GetLakeRequest.serialize,
                response_deserializer=resources.Lake.deserialize,
            )
        return self._stubs["get_lake"]

    @property
    def list_lake_actions(
        self,
    ) -> Callable[[service.ListLakeActionsRequest], service.ListActionsResponse]:
        r"""Return a callable for the list lake actions method over gRPC.

        Lists action resources in a lake.

        Returns:
            Callable[[~.ListLakeActionsRequest],
                    ~.ListActionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_lake_actions" not in self._stubs:
            self._stubs["list_lake_actions"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListLakeActions",
                request_serializer=service.ListLakeActionsRequest.serialize,
                response_deserializer=service.ListActionsResponse.deserialize,
            )
        return self._stubs["list_lake_actions"]

    @property
    def create_zone(
        self,
    ) -> Callable[[service.CreateZoneRequest], operations_pb2.Operation]:
        r"""Return a callable for the create zone method over gRPC.

        Creates a zone resource within a lake.

        Returns:
            Callable[[~.CreateZoneRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_zone" not in self._stubs:
            self._stubs["create_zone"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CreateZone",
                request_serializer=service.CreateZoneRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_zone"]

    @property
    def update_zone(
        self,
    ) -> Callable[[service.UpdateZoneRequest], operations_pb2.Operation]:
        r"""Return a callable for the update zone method over gRPC.

        Updates a zone resource.

        Returns:
            Callable[[~.UpdateZoneRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_zone" not in self._stubs:
            self._stubs["update_zone"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/UpdateZone",
                request_serializer=service.UpdateZoneRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_zone"]

    @property
    def delete_zone(
        self,
    ) -> Callable[[service.DeleteZoneRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete zone method over gRPC.

        Deletes a zone resource. All assets within a zone
        must be deleted before the zone can be deleted.

        Returns:
            Callable[[~.DeleteZoneRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_zone" not in self._stubs:
            self._stubs["delete_zone"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/DeleteZone",
                request_serializer=service.DeleteZoneRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_zone"]

    @property
    def list_zones(
        self,
    ) -> Callable[[service.ListZonesRequest], service.ListZonesResponse]:
        r"""Return a callable for the list zones method over gRPC.

        Lists zone resources in a lake.

        Returns:
            Callable[[~.ListZonesRequest],
                    ~.ListZonesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_zones" not in self._stubs:
            self._stubs["list_zones"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListZones",
                request_serializer=service.ListZonesRequest.serialize,
                response_deserializer=service.ListZonesResponse.deserialize,
            )
        return self._stubs["list_zones"]

    @property
    def get_zone(self) -> Callable[[service.GetZoneRequest], resources.Zone]:
        r"""Return a callable for the get zone method over gRPC.

        Retrieves a zone resource.

        Returns:
            Callable[[~.GetZoneRequest],
                    ~.Zone]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_zone" not in self._stubs:
            self._stubs["get_zone"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetZone",
                request_serializer=service.GetZoneRequest.serialize,
                response_deserializer=resources.Zone.deserialize,
            )
        return self._stubs["get_zone"]

    @property
    def list_zone_actions(
        self,
    ) -> Callable[[service.ListZoneActionsRequest], service.ListActionsResponse]:
        r"""Return a callable for the list zone actions method over gRPC.

        Lists action resources in a zone.

        Returns:
            Callable[[~.ListZoneActionsRequest],
                    ~.ListActionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_zone_actions" not in self._stubs:
            self._stubs["list_zone_actions"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListZoneActions",
                request_serializer=service.ListZoneActionsRequest.serialize,
                response_deserializer=service.ListActionsResponse.deserialize,
            )
        return self._stubs["list_zone_actions"]

    @property
    def create_asset(
        self,
    ) -> Callable[[service.CreateAssetRequest], operations_pb2.Operation]:
        r"""Return a callable for the create asset method over gRPC.

        Creates an asset resource.

        Returns:
            Callable[[~.CreateAssetRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_asset" not in self._stubs:
            self._stubs["create_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CreateAsset",
                request_serializer=service.CreateAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_asset"]

    @property
    def update_asset(
        self,
    ) -> Callable[[service.UpdateAssetRequest], operations_pb2.Operation]:
        r"""Return a callable for the update asset method over gRPC.

        Updates an asset resource.

        Returns:
            Callable[[~.UpdateAssetRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_asset" not in self._stubs:
            self._stubs["update_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/UpdateAsset",
                request_serializer=service.UpdateAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_asset"]

    @property
    def delete_asset(
        self,
    ) -> Callable[[service.DeleteAssetRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete asset method over gRPC.

        Deletes an asset resource. The referenced storage
        resource is detached (default) or deleted based on the
        associated Lifecycle policy.

        Returns:
            Callable[[~.DeleteAssetRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_asset" not in self._stubs:
            self._stubs["delete_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/DeleteAsset",
                request_serializer=service.DeleteAssetRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_asset"]

    @property
    def list_assets(
        self,
    ) -> Callable[[service.ListAssetsRequest], service.ListAssetsResponse]:
        r"""Return a callable for the list assets method over gRPC.

        Lists asset resources in a zone.

        Returns:
            Callable[[~.ListAssetsRequest],
                    ~.ListAssetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_assets" not in self._stubs:
            self._stubs["list_assets"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListAssets",
                request_serializer=service.ListAssetsRequest.serialize,
                response_deserializer=service.ListAssetsResponse.deserialize,
            )
        return self._stubs["list_assets"]

    @property
    def get_asset(self) -> Callable[[service.GetAssetRequest], resources.Asset]:
        r"""Return a callable for the get asset method over gRPC.

        Retrieves an asset resource.

        Returns:
            Callable[[~.GetAssetRequest],
                    ~.Asset]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_asset" not in self._stubs:
            self._stubs["get_asset"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetAsset",
                request_serializer=service.GetAssetRequest.serialize,
                response_deserializer=resources.Asset.deserialize,
            )
        return self._stubs["get_asset"]

    @property
    def list_asset_actions(
        self,
    ) -> Callable[[service.ListAssetActionsRequest], service.ListActionsResponse]:
        r"""Return a callable for the list asset actions method over gRPC.

        Lists action resources in an asset.

        Returns:
            Callable[[~.ListAssetActionsRequest],
                    ~.ListActionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_asset_actions" not in self._stubs:
            self._stubs["list_asset_actions"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListAssetActions",
                request_serializer=service.ListAssetActionsRequest.serialize,
                response_deserializer=service.ListActionsResponse.deserialize,
            )
        return self._stubs["list_asset_actions"]

    @property
    def create_task(
        self,
    ) -> Callable[[service.CreateTaskRequest], operations_pb2.Operation]:
        r"""Return a callable for the create task method over gRPC.

        Creates a task resource within a lake.

        Returns:
            Callable[[~.CreateTaskRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_task" not in self._stubs:
            self._stubs["create_task"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CreateTask",
                request_serializer=service.CreateTaskRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_task"]

    @property
    def update_task(
        self,
    ) -> Callable[[service.UpdateTaskRequest], operations_pb2.Operation]:
        r"""Return a callable for the update task method over gRPC.

        Update the task resource.

        Returns:
            Callable[[~.UpdateTaskRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_task" not in self._stubs:
            self._stubs["update_task"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/UpdateTask",
                request_serializer=service.UpdateTaskRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_task"]

    @property
    def delete_task(
        self,
    ) -> Callable[[service.DeleteTaskRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete task method over gRPC.

        Delete the task resource.

        Returns:
            Callable[[~.DeleteTaskRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_task" not in self._stubs:
            self._stubs["delete_task"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/DeleteTask",
                request_serializer=service.DeleteTaskRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_task"]

    @property
    def list_tasks(
        self,
    ) -> Callable[[service.ListTasksRequest], service.ListTasksResponse]:
        r"""Return a callable for the list tasks method over gRPC.

        Lists tasks under the given lake.

        Returns:
            Callable[[~.ListTasksRequest],
                    ~.ListTasksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_tasks" not in self._stubs:
            self._stubs["list_tasks"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListTasks",
                request_serializer=service.ListTasksRequest.serialize,
                response_deserializer=service.ListTasksResponse.deserialize,
            )
        return self._stubs["list_tasks"]

    @property
    def get_task(self) -> Callable[[service.GetTaskRequest], tasks.Task]:
        r"""Return a callable for the get task method over gRPC.

        Get task resource.

        Returns:
            Callable[[~.GetTaskRequest],
                    ~.Task]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_task" not in self._stubs:
            self._stubs["get_task"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetTask",
                request_serializer=service.GetTaskRequest.serialize,
                response_deserializer=tasks.Task.deserialize,
            )
        return self._stubs["get_task"]

    @property
    def list_jobs(
        self,
    ) -> Callable[[service.ListJobsRequest], service.ListJobsResponse]:
        r"""Return a callable for the list jobs method over gRPC.

        Lists Jobs under the given task.

        Returns:
            Callable[[~.ListJobsRequest],
                    ~.ListJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_jobs" not in self._stubs:
            self._stubs["list_jobs"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListJobs",
                request_serializer=service.ListJobsRequest.serialize,
                response_deserializer=service.ListJobsResponse.deserialize,
            )
        return self._stubs["list_jobs"]

    @property
    def run_task(self) -> Callable[[service.RunTaskRequest], service.RunTaskResponse]:
        r"""Return a callable for the run task method over gRPC.

        Run an on demand execution of a Task.

        Returns:
            Callable[[~.RunTaskRequest],
                    ~.RunTaskResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_task" not in self._stubs:
            self._stubs["run_task"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/RunTask",
                request_serializer=service.RunTaskRequest.serialize,
                response_deserializer=service.RunTaskResponse.deserialize,
            )
        return self._stubs["run_task"]

    @property
    def get_job(self) -> Callable[[service.GetJobRequest], tasks.Job]:
        r"""Return a callable for the get job method over gRPC.

        Get job resource.

        Returns:
            Callable[[~.GetJobRequest],
                    ~.Job]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job" not in self._stubs:
            self._stubs["get_job"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetJob",
                request_serializer=service.GetJobRequest.serialize,
                response_deserializer=tasks.Job.deserialize,
            )
        return self._stubs["get_job"]

    @property
    def cancel_job(self) -> Callable[[service.CancelJobRequest], empty_pb2.Empty]:
        r"""Return a callable for the cancel job method over gRPC.

        Cancel jobs running for the task resource.

        Returns:
            Callable[[~.CancelJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_job" not in self._stubs:
            self._stubs["cancel_job"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CancelJob",
                request_serializer=service.CancelJobRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["cancel_job"]

    @property
    def create_environment(
        self,
    ) -> Callable[[service.CreateEnvironmentRequest], operations_pb2.Operation]:
        r"""Return a callable for the create environment method over gRPC.

        Create an environment resource.

        Returns:
            Callable[[~.CreateEnvironmentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_environment" not in self._stubs:
            self._stubs["create_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/CreateEnvironment",
                request_serializer=service.CreateEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_environment"]

    @property
    def update_environment(
        self,
    ) -> Callable[[service.UpdateEnvironmentRequest], operations_pb2.Operation]:
        r"""Return a callable for the update environment method over gRPC.

        Update the environment resource.

        Returns:
            Callable[[~.UpdateEnvironmentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_environment" not in self._stubs:
            self._stubs["update_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/UpdateEnvironment",
                request_serializer=service.UpdateEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_environment"]

    @property
    def delete_environment(
        self,
    ) -> Callable[[service.DeleteEnvironmentRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete environment method over gRPC.

        Delete the environment resource. All the child
        resources must have been deleted before environment
        deletion can be initiated.

        Returns:
            Callable[[~.DeleteEnvironmentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_environment" not in self._stubs:
            self._stubs["delete_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/DeleteEnvironment",
                request_serializer=service.DeleteEnvironmentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_environment"]

    @property
    def list_environments(
        self,
    ) -> Callable[[service.ListEnvironmentsRequest], service.ListEnvironmentsResponse]:
        r"""Return a callable for the list environments method over gRPC.

        Lists environments under the given lake.

        Returns:
            Callable[[~.ListEnvironmentsRequest],
                    ~.ListEnvironmentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_environments" not in self._stubs:
            self._stubs["list_environments"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListEnvironments",
                request_serializer=service.ListEnvironmentsRequest.serialize,
                response_deserializer=service.ListEnvironmentsResponse.deserialize,
            )
        return self._stubs["list_environments"]

    @property
    def get_environment(
        self,
    ) -> Callable[[service.GetEnvironmentRequest], analyze.Environment]:
        r"""Return a callable for the get environment method over gRPC.

        Get environment resource.

        Returns:
            Callable[[~.GetEnvironmentRequest],
                    ~.Environment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_environment" not in self._stubs:
            self._stubs["get_environment"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/GetEnvironment",
                request_serializer=service.GetEnvironmentRequest.serialize,
                response_deserializer=analyze.Environment.deserialize,
            )
        return self._stubs["get_environment"]

    @property
    def list_sessions(
        self,
    ) -> Callable[[service.ListSessionsRequest], service.ListSessionsResponse]:
        r"""Return a callable for the list sessions method over gRPC.

        Lists session resources in an environment.

        Returns:
            Callable[[~.ListSessionsRequest],
                    ~.ListSessionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_sessions" not in self._stubs:
            self._stubs["list_sessions"] = self._logged_channel.unary_unary(
                "/google.cloud.dataplex.v1.DataplexService/ListSessions",
                request_serializer=service.ListSessionsRequest.serialize,
                response_deserializer=service.ListSessionsResponse.deserialize,
            )
        return self._stubs["list_sessions"]

    def close(self):
        self._logged_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self._logged_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("DataplexServiceGrpcTransport",)
