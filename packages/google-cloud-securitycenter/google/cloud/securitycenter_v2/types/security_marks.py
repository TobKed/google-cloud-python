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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v2",
    manifest={
        "SecurityMarks",
    },
)


class SecurityMarks(proto.Message):
    r"""User specified security marks that are attached to the parent
    Security Command Center resource. Security marks are scoped
    within a Security Command Center organization -- they can be
    modified and viewed by all users who have proper permissions on
    the organization.

    Attributes:
        name (str):
            The relative resource name of the SecurityMarks. See:
            https://cloud.google.com/apis/design/resource_names#relative_resource_name
            The following list shows some examples:

            -  ``organizations/{organization_id}/assets/{asset_id}/securityMarks``
            -

            ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}/securityMarks``
            +
            ``organizations/{organization_id}/sources/{source_id}/locations/{location}/findings/{finding_id}/securityMarks``
        marks (MutableMapping[str, str]):
            Mutable user specified security marks belonging to the
            parent resource. Constraints are as follows:

            -  Keys and values are treated as case insensitive
            -  Keys must be between 1 - 256 characters (inclusive)
            -  Keys must be letters, numbers, underscores, or dashes
            -  Values have leading and trailing whitespace trimmed,
               remaining characters must be between 1 - 4096 characters
               (inclusive)
        canonical_name (str):
            The canonical name of the marks. The following list shows
            some examples:

            -  ``organizations/{organization_id}/assets/{asset_id}/securityMarks``
            -

            ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}/securityMarks``
            +
            ``organizations/{organization_id}/sources/{source_id}/locations/{location}/findings/{finding_id}/securityMarks``

            -  ``folders/{folder_id}/assets/{asset_id}/securityMarks``
            -

            ``folders/{folder_id}/sources/{source_id}/findings/{finding_id}/securityMarks``
            +
            ``folders/{folder_id}/sources/{source_id}/locations/{location}/findings/{finding_id}/securityMarks``

            -  ``projects/{project_number}/assets/{asset_id}/securityMarks``
            -

            ``projects/{project_number}/sources/{source_id}/findings/{finding_id}/securityMarks``
            +
            ``projects/{project_number}/sources/{source_id}/locations/{location}/findings/{finding_id}/securityMarks``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    marks: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    canonical_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
