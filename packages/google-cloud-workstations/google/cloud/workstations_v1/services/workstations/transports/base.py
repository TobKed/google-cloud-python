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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, operations_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore
import google.protobuf

from google.cloud.workstations_v1 import gapic_version as package_version
from google.cloud.workstations_v1.types import workstations

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class WorkstationsTransport(abc.ABC):
    """Abstract transport class for Workstations."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "workstations.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'workstations.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.get_workstation_cluster: gapic_v1.method.wrap_method(
                self.get_workstation_cluster,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_workstation_clusters: gapic_v1.method.wrap_method(
                self.list_workstation_clusters,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_workstation_cluster: gapic_v1.method.wrap_method(
                self.create_workstation_cluster,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_workstation_cluster: gapic_v1.method.wrap_method(
                self.update_workstation_cluster,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_workstation_cluster: gapic_v1.method.wrap_method(
                self.delete_workstation_cluster,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_workstation_config: gapic_v1.method.wrap_method(
                self.get_workstation_config,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_workstation_configs: gapic_v1.method.wrap_method(
                self.list_workstation_configs,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_usable_workstation_configs: gapic_v1.method.wrap_method(
                self.list_usable_workstation_configs,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_workstation_config: gapic_v1.method.wrap_method(
                self.create_workstation_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_workstation_config: gapic_v1.method.wrap_method(
                self.update_workstation_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_workstation_config: gapic_v1.method.wrap_method(
                self.delete_workstation_config,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_workstation: gapic_v1.method.wrap_method(
                self.get_workstation,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_workstations: gapic_v1.method.wrap_method(
                self.list_workstations,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_usable_workstations: gapic_v1.method.wrap_method(
                self.list_usable_workstations,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_workstation: gapic_v1.method.wrap_method(
                self.create_workstation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_workstation: gapic_v1.method.wrap_method(
                self.update_workstation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_workstation: gapic_v1.method.wrap_method(
                self.delete_workstation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.start_workstation: gapic_v1.method.wrap_method(
                self.start_workstation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.stop_workstation: gapic_v1.method.wrap_method(
                self.stop_workstation,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.generate_access_token: gapic_v1.method.wrap_method(
                self.generate_access_token,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: gapic_v1.method.wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: gapic_v1.method.wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: gapic_v1.method.wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: gapic_v1.method.wrap_method(
                self.list_operations,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def get_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.GetWorkstationClusterRequest],
        Union[
            workstations.WorkstationCluster, Awaitable[workstations.WorkstationCluster]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_workstation_clusters(
        self,
    ) -> Callable[
        [workstations.ListWorkstationClustersRequest],
        Union[
            workstations.ListWorkstationClustersResponse,
            Awaitable[workstations.ListWorkstationClustersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationClusterRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationClusterRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_workstation_cluster(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationClusterRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_workstation_config(
        self,
    ) -> Callable[
        [workstations.GetWorkstationConfigRequest],
        Union[
            workstations.WorkstationConfig, Awaitable[workstations.WorkstationConfig]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListWorkstationConfigsRequest],
        Union[
            workstations.ListWorkstationConfigsResponse,
            Awaitable[workstations.ListWorkstationConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_usable_workstation_configs(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationConfigsRequest],
        Union[
            workstations.ListUsableWorkstationConfigsResponse,
            Awaitable[workstations.ListUsableWorkstationConfigsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_workstation_config(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_workstation_config(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_workstation_config(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationConfigRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_workstation(
        self,
    ) -> Callable[
        [workstations.GetWorkstationRequest],
        Union[workstations.Workstation, Awaitable[workstations.Workstation]],
    ]:
        raise NotImplementedError()

    @property
    def list_workstations(
        self,
    ) -> Callable[
        [workstations.ListWorkstationsRequest],
        Union[
            workstations.ListWorkstationsResponse,
            Awaitable[workstations.ListWorkstationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_usable_workstations(
        self,
    ) -> Callable[
        [workstations.ListUsableWorkstationsRequest],
        Union[
            workstations.ListUsableWorkstationsResponse,
            Awaitable[workstations.ListUsableWorkstationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_workstation(
        self,
    ) -> Callable[
        [workstations.CreateWorkstationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_workstation(
        self,
    ) -> Callable[
        [workstations.UpdateWorkstationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_workstation(
        self,
    ) -> Callable[
        [workstations.DeleteWorkstationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_workstation(
        self,
    ) -> Callable[
        [workstations.StartWorkstationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_workstation(
        self,
    ) -> Callable[
        [workstations.StopWorkstationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def generate_access_token(
        self,
    ) -> Callable[
        [workstations.GenerateAccessTokenRequest],
        Union[
            workstations.GenerateAccessTokenResponse,
            Awaitable[workstations.GenerateAccessTokenResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("WorkstationsTransport",)
