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
from google.cloud.confidentialcomputing import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.confidentialcomputing_v1.services.confidential_computing.async_client import (
    ConfidentialComputingAsyncClient,
)
from google.cloud.confidentialcomputing_v1.services.confidential_computing.client import (
    ConfidentialComputingClient,
)
from google.cloud.confidentialcomputing_v1.types.service import (
    Challenge,
    ConfidentialSpaceInfo,
    ContainerImageSignature,
    CreateChallengeRequest,
    GcpCredentials,
    SevSnpAttestation,
    SignedEntity,
    SigningAlgorithm,
    TdxCcelAttestation,
    TokenOptions,
    TokenType,
    TpmAttestation,
    VerifyAttestationRequest,
    VerifyAttestationResponse,
)

__all__ = (
    "ConfidentialComputingClient",
    "ConfidentialComputingAsyncClient",
    "Challenge",
    "ConfidentialSpaceInfo",
    "ContainerImageSignature",
    "CreateChallengeRequest",
    "GcpCredentials",
    "SevSnpAttestation",
    "SignedEntity",
    "TdxCcelAttestation",
    "TokenOptions",
    "TpmAttestation",
    "VerifyAttestationRequest",
    "VerifyAttestationResponse",
    "SigningAlgorithm",
    "TokenType",
)
