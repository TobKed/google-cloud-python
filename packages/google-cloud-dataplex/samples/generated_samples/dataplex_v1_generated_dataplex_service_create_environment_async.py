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
# Generated code. DO NOT EDIT!
#
# Snippet for CreateEnvironment
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-dataplex


# [START dataplex_v1_generated_DataplexService_CreateEnvironment_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import dataplex_v1


async def sample_create_environment():
    # Create a client
    client = dataplex_v1.DataplexServiceAsyncClient()

    # Initialize request argument(s)
    environment = dataplex_v1.Environment()
    environment.infrastructure_spec.os_image.image_version = "image_version_value"

    request = dataplex_v1.CreateEnvironmentRequest(
        parent="parent_value",
        environment_id="environment_id_value",
        environment=environment,
    )

    # Make the request
    operation = client.create_environment(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END dataplex_v1_generated_DataplexService_CreateEnvironment_async]
