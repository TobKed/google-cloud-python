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
# Snippet for GetBuild
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-build


# [START cloudbuild_v1_generated_CloudBuild_GetBuild_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud.devtools import cloudbuild_v1


def sample_get_build():
    # Create a client
    client = cloudbuild_v1.CloudBuildClient()

    # Initialize request argument(s)
    request = cloudbuild_v1.GetBuildRequest(
        project_id="project_id_value",
        id="id_value",
    )

    # Make the request
    response = client.get_build(request=request)

    # Handle the response
    print(response)

# [END cloudbuild_v1_generated_CloudBuild_GetBuild_sync]
