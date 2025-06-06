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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.baremetalsolution.v2",
    manifest={
        "NfsShare",
        "GetNfsShareRequest",
        "ListNfsSharesRequest",
        "ListNfsSharesResponse",
        "UpdateNfsShareRequest",
        "RenameNfsShareRequest",
        "CreateNfsShareRequest",
        "DeleteNfsShareRequest",
    },
)


class NfsShare(proto.Message):
    r"""An NFS share.

    Attributes:
        name (str):
            Immutable. The name of the NFS share.
        nfs_share_id (str):
            Output only. An identifier for the NFS share, generated by
            the backend. This field will be deprecated in the future,
            use ``id`` instead.
        id (str):
            Output only. An identifier for the NFS share, generated by
            the backend. This is the same value as nfs_share_id and will
            replace it in the future.
        state (google.cloud.bare_metal_solution_v2.types.NfsShare.State):
            Output only. The state of the NFS share.
        volume (str):
            Output only. The underlying volume of the
            share. Created automatically during
            provisioning.
        allowed_clients (MutableSequence[google.cloud.bare_metal_solution_v2.types.NfsShare.AllowedClient]):
            List of allowed access points.
        labels (MutableMapping[str, str]):
            Labels as key value pairs.
        requested_size_gib (int):
            The requested size, in GiB.
        storage_type (google.cloud.bare_metal_solution_v2.types.NfsShare.StorageType):
            Immutable. The storage type of the underlying
            volume.
    """

    class State(proto.Enum):
        r"""The possible states for this NFS share.

        Values:
            STATE_UNSPECIFIED (0):
                The share is in an unknown state.
            PROVISIONED (1):
                The share has been provisioned.
            CREATING (2):
                The NFS Share is being created.
            UPDATING (3):
                The NFS Share is being updated.
            DELETING (4):
                The NFS Share has been requested to be
                deleted.
        """
        STATE_UNSPECIFIED = 0
        PROVISIONED = 1
        CREATING = 2
        UPDATING = 3
        DELETING = 4

    class MountPermissions(proto.Enum):
        r"""The possible mount permissions.

        Values:
            MOUNT_PERMISSIONS_UNSPECIFIED (0):
                Permissions were not specified.
            READ (1):
                NFS share can be mount with read-only
                permissions.
            READ_WRITE (2):
                NFS share can be mount with read-write
                permissions.
        """
        MOUNT_PERMISSIONS_UNSPECIFIED = 0
        READ = 1
        READ_WRITE = 2

    class StorageType(proto.Enum):
        r"""The storage type for a volume.

        Values:
            STORAGE_TYPE_UNSPECIFIED (0):
                The storage type for this volume is unknown.
            SSD (1):
                The storage type for this volume is SSD.
            HDD (2):
                This storage type for this volume is HDD.
        """
        STORAGE_TYPE_UNSPECIFIED = 0
        SSD = 1
        HDD = 2

    class AllowedClient(proto.Message):
        r"""Represents an 'access point' for the share.

        Attributes:
            network (str):
                The network the access point sits on.
            share_ip (str):
                Output only. The IP address of the share on this network.
                Assigned automatically during provisioning based on the
                network's services_cidr.
            allowed_clients_cidr (str):
                The subnet of IP addresses permitted to
                access the share.
            mount_permissions (google.cloud.bare_metal_solution_v2.types.NfsShare.MountPermissions):
                Mount permissions.
            allow_dev (bool):
                Allow dev flag.  Which controls whether to
                allow creation of devices.
            allow_suid (bool):
                Allow the setuid flag.
            no_root_squash (bool):
                Disable root squashing, which is a feature of
                NFS. Root squash is a special mapping of the
                remote superuser (root) identity when using
                identity authentication.
            nfs_path (str):
                Output only. The path to access NFS, in
                format shareIP:/InstanceID InstanceID is the
                generated ID instead of customer provided name.
                example like "10.0.0.0:/g123456789-nfs001".
        """

        network: str = proto.Field(
            proto.STRING,
            number=1,
        )
        share_ip: str = proto.Field(
            proto.STRING,
            number=2,
        )
        allowed_clients_cidr: str = proto.Field(
            proto.STRING,
            number=3,
        )
        mount_permissions: "NfsShare.MountPermissions" = proto.Field(
            proto.ENUM,
            number=4,
            enum="NfsShare.MountPermissions",
        )
        allow_dev: bool = proto.Field(
            proto.BOOL,
            number=5,
        )
        allow_suid: bool = proto.Field(
            proto.BOOL,
            number=6,
        )
        no_root_squash: bool = proto.Field(
            proto.BOOL,
            number=7,
        )
        nfs_path: str = proto.Field(
            proto.STRING,
            number=8,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    nfs_share_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=3,
        enum=State,
    )
    volume: str = proto.Field(
        proto.STRING,
        number=4,
    )
    allowed_clients: MutableSequence[AllowedClient] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=AllowedClient,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    requested_size_gib: int = proto.Field(
        proto.INT64,
        number=7,
    )
    storage_type: StorageType = proto.Field(
        proto.ENUM,
        number=9,
        enum=StorageType,
    )


class GetNfsShareRequest(proto.Message):
    r"""Message for requesting NFS share information.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListNfsSharesRequest(proto.Message):
    r"""Message for requesting a list of NFS shares.

    Attributes:
        parent (str):
            Required. Parent value for
            ListNfsSharesRequest.
        page_size (int):
            Requested page size. The server might return
            fewer items than requested. If unspecified,
            server will pick an appropriate default.
        page_token (str):
            A token identifying a page of results from
            the server.
        filter (str):
            List filter.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListNfsSharesResponse(proto.Message):
    r"""Response message containing the list of NFS shares.

    Attributes:
        nfs_shares (MutableSequence[google.cloud.bare_metal_solution_v2.types.NfsShare]):
            The list of NFS shares.
        next_page_token (str):
            A token identifying a page of results from
            the server.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    nfs_shares: MutableSequence["NfsShare"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="NfsShare",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class UpdateNfsShareRequest(proto.Message):
    r"""Message requesting to updating an NFS share.

    Attributes:
        nfs_share (google.cloud.bare_metal_solution_v2.types.NfsShare):
            Required. The NFS share to update.

            The ``name`` field is used to identify the NFS share to
            update. Format:
            projects/{project}/locations/{location}/nfsShares/{nfs_share}
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to update. The only currently supported
            fields are: ``labels`` ``allowed_clients``
    """

    nfs_share: "NfsShare" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="NfsShare",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class RenameNfsShareRequest(proto.Message):
    r"""Message requesting rename of a server.

    Attributes:
        name (str):
            Required. The ``name`` field is used to identify the
            nfsshare. Format:
            projects/{project}/locations/{location}/nfsshares/{nfsshare}
        new_nfsshare_id (str):
            Required. The new ``id`` of the nfsshare.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    new_nfsshare_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateNfsShareRequest(proto.Message):
    r"""Message for creating an NFS share.

    Attributes:
        parent (str):
            Required. The parent project and location.
        nfs_share (google.cloud.bare_metal_solution_v2.types.NfsShare):
            Required. The NfsShare to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    nfs_share: "NfsShare" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="NfsShare",
    )


class DeleteNfsShareRequest(proto.Message):
    r"""Message for deleting an NFS share.

    Attributes:
        name (str):
            Required. The name of the NFS share to
            delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
