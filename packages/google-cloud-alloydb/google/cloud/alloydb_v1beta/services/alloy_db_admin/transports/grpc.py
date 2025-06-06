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

from google.cloud.alloydb_v1beta.types import resources, service

from .base import DEFAULT_CLIENT_INFO, AlloyDBAdminTransport

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
                    "serviceName": "google.cloud.alloydb.v1beta.AlloyDBAdmin",
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
                    "serviceName": "google.cloud.alloydb.v1beta.AlloyDBAdmin",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class AlloyDBAdminGrpcTransport(AlloyDBAdminTransport):
    """gRPC backend transport for AlloyDBAdmin.

    Service describing handlers for resources

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
        host: str = "alloydb.googleapis.com",
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
                 The hostname to connect to (default: 'alloydb.googleapis.com').
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
        host: str = "alloydb.googleapis.com",
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
    def list_clusters(
        self,
    ) -> Callable[[service.ListClustersRequest], service.ListClustersResponse]:
        r"""Return a callable for the list clusters method over gRPC.

        Lists Clusters in a given project and location.

        Returns:
            Callable[[~.ListClustersRequest],
                    ~.ListClustersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_clusters" not in self._stubs:
            self._stubs["list_clusters"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListClusters",
                request_serializer=service.ListClustersRequest.serialize,
                response_deserializer=service.ListClustersResponse.deserialize,
            )
        return self._stubs["list_clusters"]

    @property
    def get_cluster(self) -> Callable[[service.GetClusterRequest], resources.Cluster]:
        r"""Return a callable for the get cluster method over gRPC.

        Gets details of a single Cluster.

        Returns:
            Callable[[~.GetClusterRequest],
                    ~.Cluster]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_cluster" not in self._stubs:
            self._stubs["get_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GetCluster",
                request_serializer=service.GetClusterRequest.serialize,
                response_deserializer=resources.Cluster.deserialize,
            )
        return self._stubs["get_cluster"]

    @property
    def create_cluster(
        self,
    ) -> Callable[[service.CreateClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the create cluster method over gRPC.

        Creates a new Cluster in a given project and
        location.

        Returns:
            Callable[[~.CreateClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_cluster" not in self._stubs:
            self._stubs["create_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateCluster",
                request_serializer=service.CreateClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_cluster"]

    @property
    def update_cluster(
        self,
    ) -> Callable[[service.UpdateClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the update cluster method over gRPC.

        Updates the parameters of a single Cluster.

        Returns:
            Callable[[~.UpdateClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_cluster" not in self._stubs:
            self._stubs["update_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/UpdateCluster",
                request_serializer=service.UpdateClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_cluster"]

    @property
    def export_cluster(
        self,
    ) -> Callable[[service.ExportClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the export cluster method over gRPC.

        Exports data from the cluster.
        Imperative only.

        Returns:
            Callable[[~.ExportClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_cluster" not in self._stubs:
            self._stubs["export_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ExportCluster",
                request_serializer=service.ExportClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_cluster"]

    @property
    def import_cluster(
        self,
    ) -> Callable[[service.ImportClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the import cluster method over gRPC.

        Imports data to the cluster.
        Imperative only.

        Returns:
            Callable[[~.ImportClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_cluster" not in self._stubs:
            self._stubs["import_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ImportCluster",
                request_serializer=service.ImportClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_cluster"]

    @property
    def upgrade_cluster(
        self,
    ) -> Callable[[service.UpgradeClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the upgrade cluster method over gRPC.

        Upgrades a single Cluster.
        Imperative only.

        Returns:
            Callable[[~.UpgradeClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "upgrade_cluster" not in self._stubs:
            self._stubs["upgrade_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/UpgradeCluster",
                request_serializer=service.UpgradeClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["upgrade_cluster"]

    @property
    def delete_cluster(
        self,
    ) -> Callable[[service.DeleteClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete cluster method over gRPC.

        Deletes a single Cluster.

        Returns:
            Callable[[~.DeleteClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_cluster" not in self._stubs:
            self._stubs["delete_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/DeleteCluster",
                request_serializer=service.DeleteClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_cluster"]

    @property
    def promote_cluster(
        self,
    ) -> Callable[[service.PromoteClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the promote cluster method over gRPC.

        Promotes a SECONDARY cluster. This turns down
        replication from the PRIMARY cluster and promotes a
        secondary cluster into its own standalone cluster.
        Imperative only.

        Returns:
            Callable[[~.PromoteClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "promote_cluster" not in self._stubs:
            self._stubs["promote_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/PromoteCluster",
                request_serializer=service.PromoteClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["promote_cluster"]

    @property
    def switchover_cluster(
        self,
    ) -> Callable[[service.SwitchoverClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the switchover cluster method over gRPC.

        Switches the roles of PRIMARY and SECONDARY clusters
        without any data loss. This promotes the SECONDARY
        cluster to PRIMARY and sets up the original PRIMARY
        cluster to replicate from this newly promoted cluster.

        Returns:
            Callable[[~.SwitchoverClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "switchover_cluster" not in self._stubs:
            self._stubs["switchover_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/SwitchoverCluster",
                request_serializer=service.SwitchoverClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["switchover_cluster"]

    @property
    def restore_cluster(
        self,
    ) -> Callable[[service.RestoreClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the restore cluster method over gRPC.

        Creates a new Cluster in a given project and
        location, with a volume restored from the provided
        source, either a backup ID or a point-in-time and a
        source cluster.

        Returns:
            Callable[[~.RestoreClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restore_cluster" not in self._stubs:
            self._stubs["restore_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/RestoreCluster",
                request_serializer=service.RestoreClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restore_cluster"]

    @property
    def create_secondary_cluster(
        self,
    ) -> Callable[[service.CreateSecondaryClusterRequest], operations_pb2.Operation]:
        r"""Return a callable for the create secondary cluster method over gRPC.

        Creates a cluster of type SECONDARY in the given
        location using the primary cluster as the source.

        Returns:
            Callable[[~.CreateSecondaryClusterRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_secondary_cluster" not in self._stubs:
            self._stubs["create_secondary_cluster"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateSecondaryCluster",
                request_serializer=service.CreateSecondaryClusterRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_secondary_cluster"]

    @property
    def list_instances(
        self,
    ) -> Callable[[service.ListInstancesRequest], service.ListInstancesResponse]:
        r"""Return a callable for the list instances method over gRPC.

        Lists Instances in a given project and location.

        Returns:
            Callable[[~.ListInstancesRequest],
                    ~.ListInstancesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListInstances",
                request_serializer=service.ListInstancesRequest.serialize,
                response_deserializer=service.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self,
    ) -> Callable[[service.GetInstanceRequest], resources.Instance]:
        r"""Return a callable for the get instance method over gRPC.

        Gets details of a single Instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    ~.Instance]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GetInstance",
                request_serializer=service.GetInstanceRequest.serialize,
                response_deserializer=resources.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self,
    ) -> Callable[[service.CreateInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the create instance method over gRPC.

        Creates a new Instance in a given project and
        location.

        Returns:
            Callable[[~.CreateInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateInstance",
                request_serializer=service.CreateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def create_secondary_instance(
        self,
    ) -> Callable[[service.CreateSecondaryInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the create secondary instance method over gRPC.

        Creates a new SECONDARY Instance in a given project
        and location.

        Returns:
            Callable[[~.CreateSecondaryInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_secondary_instance" not in self._stubs:
            self._stubs["create_secondary_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateSecondaryInstance",
                request_serializer=service.CreateSecondaryInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_secondary_instance"]

    @property
    def batch_create_instances(
        self,
    ) -> Callable[[service.BatchCreateInstancesRequest], operations_pb2.Operation]:
        r"""Return a callable for the batch create instances method over gRPC.

        Creates new instances under the given project,
        location and cluster. There can be only one primary
        instance in a cluster. If the primary instance exists in
        the cluster as well as this request, then API will throw
        an error.
        The primary instance should exist before any read pool
        instance is created. If the primary instance is a part
        of the request payload, then the API will take care of
        creating instances in the correct order. This method is
        here to support Google-internal use cases, and is not
        meant for external customers to consume. Please do not
        start relying on it; its behavior is subject to change
        without notice.

        Returns:
            Callable[[~.BatchCreateInstancesRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_instances" not in self._stubs:
            self._stubs["batch_create_instances"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/BatchCreateInstances",
                request_serializer=service.BatchCreateInstancesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_create_instances"]

    @property
    def update_instance(
        self,
    ) -> Callable[[service.UpdateInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the update instance method over gRPC.

        Updates the parameters of a single Instance.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance" not in self._stubs:
            self._stubs["update_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/UpdateInstance",
                request_serializer=service.UpdateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_instance"]

    @property
    def delete_instance(
        self,
    ) -> Callable[[service.DeleteInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes a single Instance.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/DeleteInstance",
                request_serializer=service.DeleteInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def failover_instance(
        self,
    ) -> Callable[[service.FailoverInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the failover instance method over gRPC.

        Forces a Failover for a highly available instance.
        Failover promotes the HA standby instance as the new
        primary. Imperative only.

        Returns:
            Callable[[~.FailoverInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "failover_instance" not in self._stubs:
            self._stubs["failover_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/FailoverInstance",
                request_serializer=service.FailoverInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["failover_instance"]

    @property
    def inject_fault(
        self,
    ) -> Callable[[service.InjectFaultRequest], operations_pb2.Operation]:
        r"""Return a callable for the inject fault method over gRPC.

        Injects fault in an instance.
        Imperative only.

        Returns:
            Callable[[~.InjectFaultRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "inject_fault" not in self._stubs:
            self._stubs["inject_fault"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/InjectFault",
                request_serializer=service.InjectFaultRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["inject_fault"]

    @property
    def restart_instance(
        self,
    ) -> Callable[[service.RestartInstanceRequest], operations_pb2.Operation]:
        r"""Return a callable for the restart instance method over gRPC.

        Restart an Instance in a cluster.
        Imperative only.

        Returns:
            Callable[[~.RestartInstanceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "restart_instance" not in self._stubs:
            self._stubs["restart_instance"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/RestartInstance",
                request_serializer=service.RestartInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["restart_instance"]

    @property
    def execute_sql(
        self,
    ) -> Callable[[service.ExecuteSqlRequest], service.ExecuteSqlResponse]:
        r"""Return a callable for the execute sql method over gRPC.

        Executes a SQL statement in a database inside an
        AlloyDB instance.

        Returns:
            Callable[[~.ExecuteSqlRequest],
                    ~.ExecuteSqlResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "execute_sql" not in self._stubs:
            self._stubs["execute_sql"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ExecuteSql",
                request_serializer=service.ExecuteSqlRequest.serialize,
                response_deserializer=service.ExecuteSqlResponse.deserialize,
            )
        return self._stubs["execute_sql"]

    @property
    def list_backups(
        self,
    ) -> Callable[[service.ListBackupsRequest], service.ListBackupsResponse]:
        r"""Return a callable for the list backups method over gRPC.

        Lists Backups in a given project and location.

        Returns:
            Callable[[~.ListBackupsRequest],
                    ~.ListBackupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_backups" not in self._stubs:
            self._stubs["list_backups"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListBackups",
                request_serializer=service.ListBackupsRequest.serialize,
                response_deserializer=service.ListBackupsResponse.deserialize,
            )
        return self._stubs["list_backups"]

    @property
    def get_backup(self) -> Callable[[service.GetBackupRequest], resources.Backup]:
        r"""Return a callable for the get backup method over gRPC.

        Gets details of a single Backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    ~.Backup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_backup" not in self._stubs:
            self._stubs["get_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GetBackup",
                request_serializer=service.GetBackupRequest.serialize,
                response_deserializer=resources.Backup.deserialize,
            )
        return self._stubs["get_backup"]

    @property
    def create_backup(
        self,
    ) -> Callable[[service.CreateBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a new Backup in a given project and location.

        Returns:
            Callable[[~.CreateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_backup" not in self._stubs:
            self._stubs["create_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateBackup",
                request_serializer=service.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_backup"]

    @property
    def update_backup(
        self,
    ) -> Callable[[service.UpdateBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the update backup method over gRPC.

        Updates the parameters of a single Backup.

        Returns:
            Callable[[~.UpdateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_backup" not in self._stubs:
            self._stubs["update_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/UpdateBackup",
                request_serializer=service.UpdateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_backup"]

    @property
    def delete_backup(
        self,
    ) -> Callable[[service.DeleteBackupRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes a single Backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_backup" not in self._stubs:
            self._stubs["delete_backup"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/DeleteBackup",
                request_serializer=service.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_backup"]

    @property
    def list_supported_database_flags(
        self,
    ) -> Callable[
        [service.ListSupportedDatabaseFlagsRequest],
        service.ListSupportedDatabaseFlagsResponse,
    ]:
        r"""Return a callable for the list supported database flags method over gRPC.

        Lists SupportedDatabaseFlags for a given project and
        location.

        Returns:
            Callable[[~.ListSupportedDatabaseFlagsRequest],
                    ~.ListSupportedDatabaseFlagsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_supported_database_flags" not in self._stubs:
            self._stubs[
                "list_supported_database_flags"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListSupportedDatabaseFlags",
                request_serializer=service.ListSupportedDatabaseFlagsRequest.serialize,
                response_deserializer=service.ListSupportedDatabaseFlagsResponse.deserialize,
            )
        return self._stubs["list_supported_database_flags"]

    @property
    def generate_client_certificate(
        self,
    ) -> Callable[
        [service.GenerateClientCertificateRequest],
        service.GenerateClientCertificateResponse,
    ]:
        r"""Return a callable for the generate client certificate method over gRPC.

        Generate a client certificate signed by a Cluster CA.
        The sole purpose of this endpoint is to support AlloyDB
        connectors and the Auth Proxy client. The endpoint's
        behavior is subject to change without notice, so do not
        rely on its behavior remaining constant. Future changes
        will not break AlloyDB connectors or the Auth Proxy
        client.

        Returns:
            Callable[[~.GenerateClientCertificateRequest],
                    ~.GenerateClientCertificateResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_client_certificate" not in self._stubs:
            self._stubs[
                "generate_client_certificate"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GenerateClientCertificate",
                request_serializer=service.GenerateClientCertificateRequest.serialize,
                response_deserializer=service.GenerateClientCertificateResponse.deserialize,
            )
        return self._stubs["generate_client_certificate"]

    @property
    def get_connection_info(
        self,
    ) -> Callable[[service.GetConnectionInfoRequest], resources.ConnectionInfo]:
        r"""Return a callable for the get connection info method over gRPC.

        Get instance metadata used for a connection.

        Returns:
            Callable[[~.GetConnectionInfoRequest],
                    ~.ConnectionInfo]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_connection_info" not in self._stubs:
            self._stubs["get_connection_info"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GetConnectionInfo",
                request_serializer=service.GetConnectionInfoRequest.serialize,
                response_deserializer=resources.ConnectionInfo.deserialize,
            )
        return self._stubs["get_connection_info"]

    @property
    def list_users(
        self,
    ) -> Callable[[service.ListUsersRequest], service.ListUsersResponse]:
        r"""Return a callable for the list users method over gRPC.

        Lists Users in a given project and location.

        Returns:
            Callable[[~.ListUsersRequest],
                    ~.ListUsersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_users" not in self._stubs:
            self._stubs["list_users"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListUsers",
                request_serializer=service.ListUsersRequest.serialize,
                response_deserializer=service.ListUsersResponse.deserialize,
            )
        return self._stubs["list_users"]

    @property
    def get_user(self) -> Callable[[service.GetUserRequest], resources.User]:
        r"""Return a callable for the get user method over gRPC.

        Gets details of a single User.

        Returns:
            Callable[[~.GetUserRequest],
                    ~.User]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_user" not in self._stubs:
            self._stubs["get_user"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/GetUser",
                request_serializer=service.GetUserRequest.serialize,
                response_deserializer=resources.User.deserialize,
            )
        return self._stubs["get_user"]

    @property
    def create_user(self) -> Callable[[service.CreateUserRequest], resources.User]:
        r"""Return a callable for the create user method over gRPC.

        Creates a new User in a given project, location, and
        cluster.

        Returns:
            Callable[[~.CreateUserRequest],
                    ~.User]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_user" not in self._stubs:
            self._stubs["create_user"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/CreateUser",
                request_serializer=service.CreateUserRequest.serialize,
                response_deserializer=resources.User.deserialize,
            )
        return self._stubs["create_user"]

    @property
    def update_user(self) -> Callable[[service.UpdateUserRequest], resources.User]:
        r"""Return a callable for the update user method over gRPC.

        Updates the parameters of a single User.

        Returns:
            Callable[[~.UpdateUserRequest],
                    ~.User]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_user" not in self._stubs:
            self._stubs["update_user"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/UpdateUser",
                request_serializer=service.UpdateUserRequest.serialize,
                response_deserializer=resources.User.deserialize,
            )
        return self._stubs["update_user"]

    @property
    def delete_user(self) -> Callable[[service.DeleteUserRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete user method over gRPC.

        Deletes a single User.

        Returns:
            Callable[[~.DeleteUserRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_user" not in self._stubs:
            self._stubs["delete_user"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/DeleteUser",
                request_serializer=service.DeleteUserRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_user"]

    @property
    def list_databases(
        self,
    ) -> Callable[[service.ListDatabasesRequest], service.ListDatabasesResponse]:
        r"""Return a callable for the list databases method over gRPC.

        Lists Databases in a given project and location.

        Returns:
            Callable[[~.ListDatabasesRequest],
                    ~.ListDatabasesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_databases" not in self._stubs:
            self._stubs["list_databases"] = self._logged_channel.unary_unary(
                "/google.cloud.alloydb.v1beta.AlloyDBAdmin/ListDatabases",
                request_serializer=service.ListDatabasesRequest.serialize,
                response_deserializer=service.ListDatabasesResponse.deserialize,
            )
        return self._stubs["list_databases"]

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


__all__ = ("AlloyDBAdminGrpcTransport",)
