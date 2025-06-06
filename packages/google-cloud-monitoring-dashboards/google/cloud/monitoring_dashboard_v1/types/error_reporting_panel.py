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
    package="google.monitoring.dashboard.v1",
    manifest={
        "ErrorReportingPanel",
    },
)


class ErrorReportingPanel(proto.Message):
    r"""A widget that displays a list of error groups.

    Attributes:
        project_names (MutableSequence[str]):
            The resource name of the Google Cloud Platform project.
            Written as ``projects/{projectID}`` or
            ``projects/{projectNumber}``, where ``{projectID}`` and
            ``{projectNumber}`` can be found in the `Google Cloud
            console <https://support.google.com/cloud/answer/6158840>`__.

            Examples: ``projects/my-project-123``, ``projects/5551234``.
        services (MutableSequence[str]):
            An identifier of the service, such as the name of the
            executable, job, or Google App Engine service name. This
            field is expected to have a low number of values that are
            relatively stable over time, as opposed to ``version``,
            which can be changed whenever new code is deployed.

            Contains the service name for error reports extracted from
            Google App Engine logs or ``default`` if the App Engine
            default service is used.
        versions (MutableSequence[str]):
            Represents the source code version that the
            developer provided, which could represent a
            version label or a Git SHA-1 hash, for example.
            For App Engine standard environment, the version
            is set to the version of the app.
    """

    project_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    services: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
