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
from google.cloud.iap_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.identity_aware_proxy_admin_service import (
    IdentityAwareProxyAdminServiceAsyncClient,
    IdentityAwareProxyAdminServiceClient,
)
from .services.identity_aware_proxy_o_auth_service import (
    IdentityAwareProxyOAuthServiceAsyncClient,
    IdentityAwareProxyOAuthServiceClient,
)
from .types.service import (
    AccessDeniedPageSettings,
    AccessSettings,
    AllowedDomainsSettings,
    ApplicationSettings,
    AttributePropagationSettings,
    Brand,
    CorsSettings,
    CreateBrandRequest,
    CreateIdentityAwareProxyClientRequest,
    CreateTunnelDestGroupRequest,
    CsmSettings,
    DeleteIdentityAwareProxyClientRequest,
    DeleteTunnelDestGroupRequest,
    GcipSettings,
    GetBrandRequest,
    GetIapSettingsRequest,
    GetIdentityAwareProxyClientRequest,
    GetTunnelDestGroupRequest,
    IapSettings,
    IdentityAwareProxyClient,
    ListBrandsRequest,
    ListBrandsResponse,
    ListIdentityAwareProxyClientsRequest,
    ListIdentityAwareProxyClientsResponse,
    ListTunnelDestGroupsRequest,
    ListTunnelDestGroupsResponse,
    OAuth2,
    OAuthSettings,
    ReauthSettings,
    ResetIdentityAwareProxyClientSecretRequest,
    TunnelDestGroup,
    UpdateIapSettingsRequest,
    UpdateTunnelDestGroupRequest,
    ValidateIapAttributeExpressionRequest,
    ValidateIapAttributeExpressionResponse,
    WorkforceIdentitySettings,
)

__all__ = (
    "IdentityAwareProxyAdminServiceAsyncClient",
    "IdentityAwareProxyOAuthServiceAsyncClient",
    "AccessDeniedPageSettings",
    "AccessSettings",
    "AllowedDomainsSettings",
    "ApplicationSettings",
    "AttributePropagationSettings",
    "Brand",
    "CorsSettings",
    "CreateBrandRequest",
    "CreateIdentityAwareProxyClientRequest",
    "CreateTunnelDestGroupRequest",
    "CsmSettings",
    "DeleteIdentityAwareProxyClientRequest",
    "DeleteTunnelDestGroupRequest",
    "GcipSettings",
    "GetBrandRequest",
    "GetIapSettingsRequest",
    "GetIdentityAwareProxyClientRequest",
    "GetTunnelDestGroupRequest",
    "IapSettings",
    "IdentityAwareProxyAdminServiceClient",
    "IdentityAwareProxyClient",
    "IdentityAwareProxyOAuthServiceClient",
    "ListBrandsRequest",
    "ListBrandsResponse",
    "ListIdentityAwareProxyClientsRequest",
    "ListIdentityAwareProxyClientsResponse",
    "ListTunnelDestGroupsRequest",
    "ListTunnelDestGroupsResponse",
    "OAuth2",
    "OAuthSettings",
    "ReauthSettings",
    "ResetIdentityAwareProxyClientSecretRequest",
    "TunnelDestGroup",
    "UpdateIapSettingsRequest",
    "UpdateTunnelDestGroupRequest",
    "ValidateIapAttributeExpressionRequest",
    "ValidateIapAttributeExpressionResponse",
    "WorkforceIdentitySettings",
)
