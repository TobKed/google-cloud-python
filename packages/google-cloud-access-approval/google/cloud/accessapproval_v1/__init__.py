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
from google.cloud.accessapproval_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.access_approval import AccessApprovalAsyncClient, AccessApprovalClient
from .types.accessapproval import (
    AccessApprovalServiceAccount,
    AccessApprovalSettings,
    AccessLocations,
    AccessReason,
    ApprovalRequest,
    ApproveApprovalRequestMessage,
    ApproveDecision,
    DeleteAccessApprovalSettingsMessage,
    DismissApprovalRequestMessage,
    DismissDecision,
    EnrolledService,
    EnrollmentLevel,
    GetAccessApprovalServiceAccountMessage,
    GetAccessApprovalSettingsMessage,
    GetApprovalRequestMessage,
    InvalidateApprovalRequestMessage,
    ListApprovalRequestsMessage,
    ListApprovalRequestsResponse,
    ResourceProperties,
    SignatureInfo,
    UpdateAccessApprovalSettingsMessage,
)

__all__ = (
    "AccessApprovalAsyncClient",
    "AccessApprovalClient",
    "AccessApprovalServiceAccount",
    "AccessApprovalSettings",
    "AccessLocations",
    "AccessReason",
    "ApprovalRequest",
    "ApproveApprovalRequestMessage",
    "ApproveDecision",
    "DeleteAccessApprovalSettingsMessage",
    "DismissApprovalRequestMessage",
    "DismissDecision",
    "EnrolledService",
    "EnrollmentLevel",
    "GetAccessApprovalServiceAccountMessage",
    "GetAccessApprovalSettingsMessage",
    "GetApprovalRequestMessage",
    "InvalidateApprovalRequestMessage",
    "ListApprovalRequestsMessage",
    "ListApprovalRequestsResponse",
    "ResourceProperties",
    "SignatureInfo",
    "UpdateAccessApprovalSettingsMessage",
)
