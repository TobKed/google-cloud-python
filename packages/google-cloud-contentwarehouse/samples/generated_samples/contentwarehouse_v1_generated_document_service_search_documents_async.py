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
# Snippet for SearchDocuments
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-contentwarehouse


# [START contentwarehouse_v1_generated_DocumentService_SearchDocuments_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import contentwarehouse_v1


async def sample_search_documents():
    # Create a client
    client = contentwarehouse_v1.DocumentServiceAsyncClient()

    # Initialize request argument(s)
    request = contentwarehouse_v1.SearchDocumentsRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.search_documents(request=request)

    # Handle the response
    async for response in page_result:
        print(response)

# [END contentwarehouse_v1_generated_DocumentService_SearchDocuments_async]
