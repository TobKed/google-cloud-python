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
        "CollapsibleGroup",
    },
)


class CollapsibleGroup(proto.Message):
    r"""A widget that groups the other widgets. All widgets that are
    within the area spanned by the grouping widget are considered
    member widgets.

    Attributes:
        collapsed (bool):
            The collapsed state of the widget on first
            page load.
    """

    collapsed: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
