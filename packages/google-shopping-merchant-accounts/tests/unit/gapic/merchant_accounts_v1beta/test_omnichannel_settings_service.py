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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import AsyncIterable, Iterable
import json
import math

from google.api_core import api_core_version
from google.protobuf import json_format
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

try:
    from google.auth.aio import credentials as ga_credentials_async

    HAS_GOOGLE_AUTH_AIO = True
except ImportError:  # pragma: NO COVER
    HAS_GOOGLE_AUTH_AIO = False

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore

from google.shopping.merchant_accounts_v1beta.services.omnichannel_settings_service import (
    OmnichannelSettingsServiceAsyncClient,
    OmnichannelSettingsServiceClient,
    pagers,
    transports,
)
from google.shopping.merchant_accounts_v1beta.types import omnichannelsettings

CRED_INFO_JSON = {
    "credential_source": "/path/to/file",
    "credential_type": "service account credentials",
    "principal": "service-account@example.com",
}
CRED_INFO_STRING = json.dumps(CRED_INFO_JSON)


async def mock_async_gen(data, chunk_size=1):
    for i in range(0, len(data)):  # pragma: NO COVER
        chunk = data[i : i + chunk_size]
        yield chunk.encode("utf-8")


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# TODO: use async auth anon credentials by default once the minimum version of google-auth is upgraded.
# See related issue: https://github.com/googleapis/gapic-generator-python/issues/2107.
def async_anonymous_credentials():
    if HAS_GOOGLE_AUTH_AIO:
        return ga_credentials_async.AnonymousCredentials()
    return ga_credentials.AnonymousCredentials()


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert OmnichannelSettingsServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        OmnichannelSettingsServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert OmnichannelSettingsServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            OmnichannelSettingsServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            OmnichannelSettingsServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert OmnichannelSettingsServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert OmnichannelSettingsServiceClient._get_client_cert_source(None, False) is None
    assert (
        OmnichannelSettingsServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        OmnichannelSettingsServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                OmnichannelSettingsServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                OmnichannelSettingsServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    OmnichannelSettingsServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceClient),
)
@mock.patch.object(
    OmnichannelSettingsServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = OmnichannelSettingsServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        OmnichannelSettingsServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = OmnichannelSettingsServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == OmnichannelSettingsServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == OmnichannelSettingsServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == OmnichannelSettingsServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        OmnichannelSettingsServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        OmnichannelSettingsServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        OmnichannelSettingsServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        OmnichannelSettingsServiceClient._get_universe_domain(None, None)
        == OmnichannelSettingsServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        OmnichannelSettingsServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "error_code,cred_info_json,show_cred_info",
    [
        (401, CRED_INFO_JSON, True),
        (403, CRED_INFO_JSON, True),
        (404, CRED_INFO_JSON, True),
        (500, CRED_INFO_JSON, False),
        (401, None, False),
        (403, None, False),
        (404, None, False),
        (500, None, False),
    ],
)
def test__add_cred_info_for_auth_errors(error_code, cred_info_json, show_cred_info):
    cred = mock.Mock(["get_cred_info"])
    cred.get_cred_info = mock.Mock(return_value=cred_info_json)
    client = OmnichannelSettingsServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=["foo"])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    if show_cred_info:
        assert error.details == ["foo", CRED_INFO_STRING]
    else:
        assert error.details == ["foo"]


@pytest.mark.parametrize("error_code", [401, 403, 404, 500])
def test__add_cred_info_for_auth_errors_no_get_cred_info(error_code):
    cred = mock.Mock([])
    assert not hasattr(cred, "get_cred_info")
    client = OmnichannelSettingsServiceClient(credentials=cred)
    client._transport._credentials = cred

    error = core_exceptions.GoogleAPICallError("message", details=[])
    error.code = error_code

    client._add_cred_info_for_auth_errors(error)
    assert error.details == []


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OmnichannelSettingsServiceClient, "grpc"),
        (OmnichannelSettingsServiceAsyncClient, "grpc_asyncio"),
        (OmnichannelSettingsServiceClient, "rest"),
    ],
)
def test_omnichannel_settings_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "merchantapi.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://merchantapi.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.OmnichannelSettingsServiceGrpcTransport, "grpc"),
        (transports.OmnichannelSettingsServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.OmnichannelSettingsServiceRestTransport, "rest"),
    ],
)
def test_omnichannel_settings_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (OmnichannelSettingsServiceClient, "grpc"),
        (OmnichannelSettingsServiceAsyncClient, "grpc_asyncio"),
        (OmnichannelSettingsServiceClient, "rest"),
    ],
)
def test_omnichannel_settings_service_client_from_service_account_file(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "merchantapi.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://merchantapi.googleapis.com"
        )


def test_omnichannel_settings_service_client_get_transport_class():
    transport = OmnichannelSettingsServiceClient.get_transport_class()
    available_transports = [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceRestTransport,
    ]
    assert transport in available_transports

    transport = OmnichannelSettingsServiceClient.get_transport_class("grpc")
    assert transport == transports.OmnichannelSettingsServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    OmnichannelSettingsServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceClient),
)
@mock.patch.object(
    OmnichannelSettingsServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceAsyncClient),
)
def test_omnichannel_settings_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        OmnichannelSettingsServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        OmnichannelSettingsServiceClient, "get_transport_class"
    ) as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceRestTransport,
            "rest",
            "true",
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    OmnichannelSettingsServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceClient),
)
@mock.patch.object(
    OmnichannelSettingsServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_omnichannel_settings_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class",
    [OmnichannelSettingsServiceClient, OmnichannelSettingsServiceAsyncClient],
)
@mock.patch.object(
    OmnichannelSettingsServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OmnichannelSettingsServiceClient),
)
@mock.patch.object(
    OmnichannelSettingsServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OmnichannelSettingsServiceAsyncClient),
)
def test_omnichannel_settings_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class",
    [OmnichannelSettingsServiceClient, OmnichannelSettingsServiceAsyncClient],
)
@mock.patch.object(
    OmnichannelSettingsServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceClient),
)
@mock.patch.object(
    OmnichannelSettingsServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(OmnichannelSettingsServiceAsyncClient),
)
def test_omnichannel_settings_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = OmnichannelSettingsServiceClient._DEFAULT_UNIVERSE
    default_endpoint = (
        OmnichannelSettingsServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
            UNIVERSE_DOMAIN=default_universe
        )
    )
    mock_universe = "bar.com"
    mock_endpoint = OmnichannelSettingsServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceRestTransport,
            "rest",
        ),
    ],
)
def test_omnichannel_settings_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_omnichannel_settings_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_omnichannel_settings_service_client_client_options_from_dict():
    with mock.patch(
        "google.shopping.merchant_accounts_v1beta.services.omnichannel_settings_service.transports.OmnichannelSettingsServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OmnichannelSettingsServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_omnichannel_settings_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "merchantapi.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            scopes=None,
            default_host="merchantapi.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.GetOmnichannelSettingRequest,
        dict,
    ],
)
def test_get_omnichannel_setting(request_type, transport: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )
        response = client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.GetOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


def test_get_omnichannel_setting_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = omnichannelsettings.GetOmnichannelSettingRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_omnichannel_setting(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == omnichannelsettings.GetOmnichannelSettingRequest(
            name="name_value",
        )


def test_get_omnichannel_setting_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_omnichannel_setting
        ] = mock_rpc
        request = {}
        client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_omnichannel_setting_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_omnichannel_setting
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_omnichannel_setting
        ] = mock_rpc

        request = {}
        await client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.get_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_omnichannel_setting_async(
    transport: str = "grpc_asyncio",
    request_type=omnichannelsettings.GetOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        response = await client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.GetOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.asyncio
async def test_get_omnichannel_setting_async_from_dict():
    await test_get_omnichannel_setting_async(request_type=dict)


def test_get_omnichannel_setting_field_headers():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.GetOmnichannelSettingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_omnichannel_setting_field_headers_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.GetOmnichannelSettingRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        await client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_omnichannel_setting_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_omnichannel_setting(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_omnichannel_setting_flattened_error():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_omnichannel_setting(
            omnichannelsettings.GetOmnichannelSettingRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_omnichannel_setting_flattened_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_omnichannel_setting(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_omnichannel_setting_flattened_error_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_omnichannel_setting(
            omnichannelsettings.GetOmnichannelSettingRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.ListOmnichannelSettingsRequest,
        dict,
    ],
)
def test_list_omnichannel_settings(request_type, transport: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.ListOmnichannelSettingsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.ListOmnichannelSettingsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOmnichannelSettingsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_omnichannel_settings_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = omnichannelsettings.ListOmnichannelSettingsRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_omnichannel_settings(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == omnichannelsettings.ListOmnichannelSettingsRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_omnichannel_settings_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_omnichannel_settings
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_omnichannel_settings
        ] = mock_rpc
        request = {}
        client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_omnichannel_settings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_omnichannel_settings_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_omnichannel_settings
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_omnichannel_settings
        ] = mock_rpc

        request = {}
        await client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_omnichannel_settings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_omnichannel_settings_async(
    transport: str = "grpc_asyncio",
    request_type=omnichannelsettings.ListOmnichannelSettingsRequest,
):
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.ListOmnichannelSettingsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.ListOmnichannelSettingsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOmnichannelSettingsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_omnichannel_settings_async_from_dict():
    await test_list_omnichannel_settings_async(request_type=dict)


def test_list_omnichannel_settings_field_headers():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.ListOmnichannelSettingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.ListOmnichannelSettingsResponse()
        client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_omnichannel_settings_field_headers_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.ListOmnichannelSettingsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.ListOmnichannelSettingsResponse()
        )
        await client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_omnichannel_settings_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.ListOmnichannelSettingsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_omnichannel_settings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_omnichannel_settings_flattened_error():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_omnichannel_settings(
            omnichannelsettings.ListOmnichannelSettingsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_omnichannel_settings_flattened_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.ListOmnichannelSettingsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.ListOmnichannelSettingsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_omnichannel_settings(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_omnichannel_settings_flattened_error_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_omnichannel_settings(
            omnichannelsettings.ListOmnichannelSettingsRequest(),
            parent="parent_value",
        )


def test_list_omnichannel_settings_pager(transport_name: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="abc",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[],
                next_page_token="def",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="ghi",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_omnichannel_settings(
            request={}, retry=retry, timeout=timeout
        )

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, omnichannelsettings.OmnichannelSetting) for i in results
        )


def test_list_omnichannel_settings_pages(transport_name: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="abc",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[],
                next_page_token="def",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="ghi",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_omnichannel_settings(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_omnichannel_settings_async_pager():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="abc",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[],
                next_page_token="def",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="ghi",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_omnichannel_settings(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, omnichannelsettings.OmnichannelSetting) for i in responses
        )


@pytest.mark.asyncio
async def test_list_omnichannel_settings_async_pages():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="abc",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[],
                next_page_token="def",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="ghi",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_omnichannel_settings(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.CreateOmnichannelSettingRequest,
        dict,
    ],
)
def test_create_omnichannel_setting(request_type, transport: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )
        response = client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.CreateOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


def test_create_omnichannel_setting_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = omnichannelsettings.CreateOmnichannelSettingRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_omnichannel_setting(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == omnichannelsettings.CreateOmnichannelSettingRequest(
            parent="parent_value",
        )


def test_create_omnichannel_setting_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_omnichannel_setting
        ] = mock_rpc
        request = {}
        client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_omnichannel_setting_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_omnichannel_setting
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_omnichannel_setting
        ] = mock_rpc

        request = {}
        await client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.create_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_omnichannel_setting_async(
    transport: str = "grpc_asyncio",
    request_type=omnichannelsettings.CreateOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        response = await client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.CreateOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.asyncio
async def test_create_omnichannel_setting_async_from_dict():
    await test_create_omnichannel_setting_async(request_type=dict)


def test_create_omnichannel_setting_field_headers():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.CreateOmnichannelSettingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_omnichannel_setting_field_headers_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.CreateOmnichannelSettingRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        await client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_omnichannel_setting_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_omnichannel_setting(
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].omnichannel_setting
        mock_val = omnichannelsettings.OmnichannelSetting(name="name_value")
        assert arg == mock_val


def test_create_omnichannel_setting_flattened_error():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_omnichannel_setting(
            omnichannelsettings.CreateOmnichannelSettingRequest(),
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )


@pytest.mark.asyncio
async def test_create_omnichannel_setting_flattened_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_omnichannel_setting(
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].omnichannel_setting
        mock_val = omnichannelsettings.OmnichannelSetting(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_omnichannel_setting_flattened_error_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_omnichannel_setting(
            omnichannelsettings.CreateOmnichannelSettingRequest(),
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.UpdateOmnichannelSettingRequest,
        dict,
    ],
)
def test_update_omnichannel_setting(request_type, transport: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )
        response = client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.UpdateOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


def test_update_omnichannel_setting_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = omnichannelsettings.UpdateOmnichannelSettingRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_omnichannel_setting(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == omnichannelsettings.UpdateOmnichannelSettingRequest()


def test_update_omnichannel_setting_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_omnichannel_setting
        ] = mock_rpc
        request = {}
        client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_omnichannel_setting_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_omnichannel_setting
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_omnichannel_setting
        ] = mock_rpc

        request = {}
        await client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.update_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_omnichannel_setting_async(
    transport: str = "grpc_asyncio",
    request_type=omnichannelsettings.UpdateOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        response = await client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.UpdateOmnichannelSettingRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.asyncio
async def test_update_omnichannel_setting_async_from_dict():
    await test_update_omnichannel_setting_async(request_type=dict)


def test_update_omnichannel_setting_field_headers():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.UpdateOmnichannelSettingRequest()

    request.omnichannel_setting.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "omnichannel_setting.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_omnichannel_setting_field_headers_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.UpdateOmnichannelSettingRequest()

    request.omnichannel_setting.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        await client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "omnichannel_setting.name=name_value",
    ) in kw["metadata"]


def test_update_omnichannel_setting_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_omnichannel_setting(
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].omnichannel_setting
        mock_val = omnichannelsettings.OmnichannelSetting(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_omnichannel_setting_flattened_error():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_omnichannel_setting(
            omnichannelsettings.UpdateOmnichannelSettingRequest(),
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_omnichannel_setting_flattened_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.OmnichannelSetting()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_omnichannel_setting(
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].omnichannel_setting
        mock_val = omnichannelsettings.OmnichannelSetting(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_omnichannel_setting_flattened_error_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_omnichannel_setting(
            omnichannelsettings.UpdateOmnichannelSettingRequest(),
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.RequestInventoryVerificationRequest,
        dict,
    ],
)
def test_request_inventory_verification(request_type, transport: str = "grpc"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.RequestInventoryVerificationResponse()
        response = client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.RequestInventoryVerificationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, omnichannelsettings.RequestInventoryVerificationResponse
    )


def test_request_inventory_verification_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = omnichannelsettings.RequestInventoryVerificationRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.request_inventory_verification(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == omnichannelsettings.RequestInventoryVerificationRequest(
            name="name_value",
        )


def test_request_inventory_verification_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.request_inventory_verification
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.request_inventory_verification
        ] = mock_rpc
        request = {}
        client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.request_inventory_verification(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_request_inventory_verification_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceAsyncClient(
            credentials=async_anonymous_credentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.request_inventory_verification
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[
            client._client._transport.request_inventory_verification
        ] = mock_rpc

        request = {}
        await client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.request_inventory_verification(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_request_inventory_verification_async(
    transport: str = "grpc_asyncio",
    request_type=omnichannelsettings.RequestInventoryVerificationRequest,
):
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.RequestInventoryVerificationResponse()
        )
        response = await client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = omnichannelsettings.RequestInventoryVerificationRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, omnichannelsettings.RequestInventoryVerificationResponse
    )


@pytest.mark.asyncio
async def test_request_inventory_verification_async_from_dict():
    await test_request_inventory_verification_async(request_type=dict)


def test_request_inventory_verification_field_headers():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.RequestInventoryVerificationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.RequestInventoryVerificationResponse()
        client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_request_inventory_verification_field_headers_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = omnichannelsettings.RequestInventoryVerificationRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.RequestInventoryVerificationResponse()
        )
        await client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_request_inventory_verification_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.RequestInventoryVerificationResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.request_inventory_verification(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_request_inventory_verification_flattened_error():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.request_inventory_verification(
            omnichannelsettings.RequestInventoryVerificationRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_request_inventory_verification_flattened_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = omnichannelsettings.RequestInventoryVerificationResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.RequestInventoryVerificationResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.request_inventory_verification(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_request_inventory_verification_flattened_error_async():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.request_inventory_verification(
            omnichannelsettings.RequestInventoryVerificationRequest(),
            name="name_value",
        )


def test_get_omnichannel_setting_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_omnichannel_setting
        ] = mock_rpc

        request = {}
        client.get_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_omnichannel_setting_rest_required_fields(
    request_type=omnichannelsettings.GetOmnichannelSettingRequest,
):
    transport_class = transports.OmnichannelSettingsServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_omnichannel_setting._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_omnichannel_setting._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = omnichannelsettings.OmnichannelSetting()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.get_omnichannel_setting(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_omnichannel_setting_rest_unset_required_fields():
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_omnichannel_setting._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_get_omnichannel_setting_rest_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "accounts/sample1/omnichannelSettings/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.get_omnichannel_setting(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/accounts/v1beta/{name=accounts/*/omnichannelSettings/*}"
            % client.transport._host,
            args[1],
        )


def test_get_omnichannel_setting_rest_flattened_error(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_omnichannel_setting(
            omnichannelsettings.GetOmnichannelSettingRequest(),
            name="name_value",
        )


def test_list_omnichannel_settings_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_omnichannel_settings
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_omnichannel_settings
        ] = mock_rpc

        request = {}
        client.list_omnichannel_settings(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_omnichannel_settings(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_omnichannel_settings_rest_required_fields(
    request_type=omnichannelsettings.ListOmnichannelSettingsRequest,
):
    transport_class = transports.OmnichannelSettingsServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_omnichannel_settings._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_omnichannel_settings._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = omnichannelsettings.ListOmnichannelSettingsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = omnichannelsettings.ListOmnichannelSettingsResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.list_omnichannel_settings(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_omnichannel_settings_rest_unset_required_fields():
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_omnichannel_settings._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


def test_list_omnichannel_settings_rest_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.ListOmnichannelSettingsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "accounts/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = omnichannelsettings.ListOmnichannelSettingsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.list_omnichannel_settings(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/accounts/v1beta/{parent=accounts/*}/omnichannelSettings"
            % client.transport._host,
            args[1],
        )


def test_list_omnichannel_settings_rest_flattened_error(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_omnichannel_settings(
            omnichannelsettings.ListOmnichannelSettingsRequest(),
            parent="parent_value",
        )


def test_list_omnichannel_settings_rest_pager(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="abc",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[],
                next_page_token="def",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                ],
                next_page_token="ghi",
            ),
            omnichannelsettings.ListOmnichannelSettingsResponse(
                omnichannel_settings=[
                    omnichannelsettings.OmnichannelSetting(),
                    omnichannelsettings.OmnichannelSetting(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            omnichannelsettings.ListOmnichannelSettingsResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "accounts/sample1"}

        pager = client.list_omnichannel_settings(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(
            isinstance(i, omnichannelsettings.OmnichannelSetting) for i in results
        )

        pages = list(client.list_omnichannel_settings(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_create_omnichannel_setting_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_omnichannel_setting
        ] = mock_rpc

        request = {}
        client.create_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_omnichannel_setting_rest_required_fields(
    request_type=omnichannelsettings.CreateOmnichannelSettingRequest,
):
    transport_class = transports.OmnichannelSettingsServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_omnichannel_setting._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_omnichannel_setting._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = omnichannelsettings.OmnichannelSetting()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.create_omnichannel_setting(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_omnichannel_setting_rest_unset_required_fields():
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_omnichannel_setting._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "omnichannelSetting",
            )
        )
    )


def test_create_omnichannel_setting_rest_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "accounts/sample1"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.create_omnichannel_setting(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/accounts/v1beta/{parent=accounts/*}/omnichannelSettings"
            % client.transport._host,
            args[1],
        )


def test_create_omnichannel_setting_rest_flattened_error(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_omnichannel_setting(
            omnichannelsettings.CreateOmnichannelSettingRequest(),
            parent="parent_value",
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
        )


def test_update_omnichannel_setting_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_omnichannel_setting
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_omnichannel_setting
        ] = mock_rpc

        request = {}
        client.update_omnichannel_setting(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_omnichannel_setting(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_omnichannel_setting_rest_required_fields(
    request_type=omnichannelsettings.UpdateOmnichannelSettingRequest,
):
    transport_class = transports.OmnichannelSettingsServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_omnichannel_setting._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_omnichannel_setting._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = omnichannelsettings.OmnichannelSetting()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "patch",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.update_omnichannel_setting(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_omnichannel_setting_rest_unset_required_fields():
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_omnichannel_setting._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(("updateMask",))
        & set(
            (
                "omnichannelSetting",
                "updateMask",
            )
        )
    )


def test_update_omnichannel_setting_rest_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "omnichannel_setting": {
                "name": "accounts/sample1/omnichannelSettings/sample2"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.update_omnichannel_setting(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/accounts/v1beta/{omnichannel_setting.name=accounts/*/omnichannelSettings/*}"
            % client.transport._host,
            args[1],
        )


def test_update_omnichannel_setting_rest_flattened_error(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_omnichannel_setting(
            omnichannelsettings.UpdateOmnichannelSettingRequest(),
            omnichannel_setting=omnichannelsettings.OmnichannelSetting(
                name="name_value"
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_request_inventory_verification_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.request_inventory_verification
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.request_inventory_verification
        ] = mock_rpc

        request = {}
        client.request_inventory_verification(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.request_inventory_verification(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_request_inventory_verification_rest_required_fields(
    request_type=omnichannelsettings.RequestInventoryVerificationRequest,
):
    transport_class = transports.OmnichannelSettingsServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).request_inventory_verification._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).request_inventory_verification._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = omnichannelsettings.RequestInventoryVerificationResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = omnichannelsettings.RequestInventoryVerificationResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value
            req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

            response = client.request_inventory_verification(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_request_inventory_verification_rest_unset_required_fields():
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.request_inventory_verification._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


def test_request_inventory_verification_rest_flattened():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.RequestInventoryVerificationResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"name": "accounts/sample1/omnichannelSettings/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = omnichannelsettings.RequestInventoryVerificationResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}

        client.request_inventory_verification(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/accounts/v1beta/{name=accounts/*/omnichannelSettings/*}:requestInventoryVerification"
            % client.transport._host,
            args[1],
        )


def test_request_inventory_verification_rest_flattened_error(transport: str = "rest"):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.request_inventory_verification(
            omnichannelsettings.RequestInventoryVerificationRequest(),
            name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OmnichannelSettingsServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OmnichannelSettingsServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = OmnichannelSettingsServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OmnichannelSettingsServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OmnichannelSettingsServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
        transports.OmnichannelSettingsServiceRestTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_kind_grpc():
    transport = OmnichannelSettingsServiceClient.get_transport_class("grpc")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "grpc"


def test_initialize_client_w_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_omnichannel_setting_empty_call_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.get_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.GetOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_omnichannel_settings_empty_call_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.ListOmnichannelSettingsResponse()
        client.list_omnichannel_settings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.ListOmnichannelSettingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_omnichannel_setting_empty_call_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.create_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.CreateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_omnichannel_setting_empty_call_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.OmnichannelSetting()
        client.update_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.UpdateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_request_inventory_verification_empty_call_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        call.return_value = omnichannelsettings.RequestInventoryVerificationResponse()
        client.request_inventory_verification(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.RequestInventoryVerificationRequest()

        assert args[0] == request_msg


def test_transport_kind_grpc_asyncio():
    transport = OmnichannelSettingsServiceAsyncClient.get_transport_class(
        "grpc_asyncio"
    )(credentials=async_anonymous_credentials())
    assert transport.kind == "grpc_asyncio"


def test_initialize_client_w_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_get_omnichannel_setting_empty_call_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        await client.get_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.GetOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_list_omnichannel_settings_empty_call_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.ListOmnichannelSettingsResponse(
                next_page_token="next_page_token_value",
            )
        )
        await client.list_omnichannel_settings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.ListOmnichannelSettingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_create_omnichannel_setting_empty_call_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        await client.create_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.CreateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_update_omnichannel_setting_empty_call_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.OmnichannelSetting(
                name="name_value",
                region_code="region_code_value",
                lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
            )
        )
        await client.update_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.UpdateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
@pytest.mark.asyncio
async def test_request_inventory_verification_empty_call_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            omnichannelsettings.RequestInventoryVerificationResponse()
        )
        await client.request_inventory_verification(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.RequestInventoryVerificationRequest()

        assert args[0] == request_msg


def test_transport_kind_rest():
    transport = OmnichannelSettingsServiceClient.get_transport_class("rest")(
        credentials=ga_credentials.AnonymousCredentials()
    )
    assert transport.kind == "rest"


def test_get_omnichannel_setting_rest_bad_request(
    request_type=omnichannelsettings.GetOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/omnichannelSettings/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.get_omnichannel_setting(request)


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.GetOmnichannelSettingRequest,
        dict,
    ],
)
def test_get_omnichannel_setting_rest_call_success(request_type):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/omnichannelSettings/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.get_omnichannel_setting(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_omnichannel_setting_rest_interceptors(null_interceptor):
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OmnichannelSettingsServiceRestInterceptor(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_get_omnichannel_setting",
    ) as post, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_get_omnichannel_setting_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "pre_get_omnichannel_setting",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = omnichannelsettings.GetOmnichannelSettingRequest.pb(
            omnichannelsettings.GetOmnichannelSettingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = omnichannelsettings.OmnichannelSetting.to_json(
            omnichannelsettings.OmnichannelSetting()
        )
        req.return_value.content = return_value

        request = omnichannelsettings.GetOmnichannelSettingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = omnichannelsettings.OmnichannelSetting()
        post_with_metadata.return_value = (
            omnichannelsettings.OmnichannelSetting(),
            metadata,
        )

        client.get_omnichannel_setting(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_list_omnichannel_settings_rest_bad_request(
    request_type=omnichannelsettings.ListOmnichannelSettingsRequest,
):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.list_omnichannel_settings(request)


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.ListOmnichannelSettingsRequest,
        dict,
    ],
)
def test_list_omnichannel_settings_rest_call_success(request_type):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.ListOmnichannelSettingsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = omnichannelsettings.ListOmnichannelSettingsResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.list_omnichannel_settings(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOmnichannelSettingsPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_omnichannel_settings_rest_interceptors(null_interceptor):
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OmnichannelSettingsServiceRestInterceptor(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_list_omnichannel_settings",
    ) as post, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_list_omnichannel_settings_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "pre_list_omnichannel_settings",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = omnichannelsettings.ListOmnichannelSettingsRequest.pb(
            omnichannelsettings.ListOmnichannelSettingsRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = omnichannelsettings.ListOmnichannelSettingsResponse.to_json(
            omnichannelsettings.ListOmnichannelSettingsResponse()
        )
        req.return_value.content = return_value

        request = omnichannelsettings.ListOmnichannelSettingsRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = omnichannelsettings.ListOmnichannelSettingsResponse()
        post_with_metadata.return_value = (
            omnichannelsettings.ListOmnichannelSettingsResponse(),
            metadata,
        )

        client.list_omnichannel_settings(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_create_omnichannel_setting_rest_bad_request(
    request_type=omnichannelsettings.CreateOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.create_omnichannel_setting(request)


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.CreateOmnichannelSettingRequest,
        dict,
    ],
)
def test_create_omnichannel_setting_rest_call_success(request_type):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "accounts/sample1"}
    request_init["omnichannel_setting"] = {
        "name": "name_value",
        "region_code": "region_code_value",
        "lsf_type": 1,
        "in_stock": {"uri": "uri_value", "state": 1},
        "pickup": {"uri": "uri_value", "state": 1},
        "lfp_link": {
            "lfp_provider": "lfp_provider_value",
            "external_account_id": "external_account_id_value",
            "state": 1,
        },
        "odo": {"uri": "uri_value", "state": 1},
        "about": {"uri": "uri_value", "state": 1},
        "inventory_verification": {
            "state": 1,
            "contact": "contact_value",
            "contact_email": "contact_email_value",
            "contact_state": 1,
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = omnichannelsettings.CreateOmnichannelSettingRequest.meta.fields[
        "omnichannel_setting"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["omnichannel_setting"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["omnichannel_setting"][field])):
                    del request_init["omnichannel_setting"][field][i][subfield]
            else:
                del request_init["omnichannel_setting"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.create_omnichannel_setting(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_omnichannel_setting_rest_interceptors(null_interceptor):
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OmnichannelSettingsServiceRestInterceptor(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_create_omnichannel_setting",
    ) as post, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_create_omnichannel_setting_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "pre_create_omnichannel_setting",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = omnichannelsettings.CreateOmnichannelSettingRequest.pb(
            omnichannelsettings.CreateOmnichannelSettingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = omnichannelsettings.OmnichannelSetting.to_json(
            omnichannelsettings.OmnichannelSetting()
        )
        req.return_value.content = return_value

        request = omnichannelsettings.CreateOmnichannelSettingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = omnichannelsettings.OmnichannelSetting()
        post_with_metadata.return_value = (
            omnichannelsettings.OmnichannelSetting(),
            metadata,
        )

        client.create_omnichannel_setting(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_update_omnichannel_setting_rest_bad_request(
    request_type=omnichannelsettings.UpdateOmnichannelSettingRequest,
):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {
        "omnichannel_setting": {"name": "accounts/sample1/omnichannelSettings/sample2"}
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.update_omnichannel_setting(request)


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.UpdateOmnichannelSettingRequest,
        dict,
    ],
)
def test_update_omnichannel_setting_rest_call_success(request_type):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {
        "omnichannel_setting": {"name": "accounts/sample1/omnichannelSettings/sample2"}
    }
    request_init["omnichannel_setting"] = {
        "name": "accounts/sample1/omnichannelSettings/sample2",
        "region_code": "region_code_value",
        "lsf_type": 1,
        "in_stock": {"uri": "uri_value", "state": 1},
        "pickup": {"uri": "uri_value", "state": 1},
        "lfp_link": {
            "lfp_provider": "lfp_provider_value",
            "external_account_id": "external_account_id_value",
            "state": 1,
        },
        "odo": {"uri": "uri_value", "state": 1},
        "about": {"uri": "uri_value", "state": 1},
        "inventory_verification": {
            "state": 1,
            "contact": "contact_value",
            "contact_email": "contact_email_value",
            "contact_state": 1,
        },
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = omnichannelsettings.UpdateOmnichannelSettingRequest.meta.fields[
        "omnichannel_setting"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["omnichannel_setting"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["omnichannel_setting"][field])):
                    del request_init["omnichannel_setting"][field][i][subfield]
            else:
                del request_init["omnichannel_setting"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.OmnichannelSetting(
            name="name_value",
            region_code="region_code_value",
            lsf_type=omnichannelsettings.OmnichannelSetting.LsfType.GHLSF,
        )

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = omnichannelsettings.OmnichannelSetting.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.update_omnichannel_setting(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, omnichannelsettings.OmnichannelSetting)
    assert response.name == "name_value"
    assert response.region_code == "region_code_value"
    assert response.lsf_type == omnichannelsettings.OmnichannelSetting.LsfType.GHLSF


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_omnichannel_setting_rest_interceptors(null_interceptor):
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OmnichannelSettingsServiceRestInterceptor(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_update_omnichannel_setting",
    ) as post, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_update_omnichannel_setting_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "pre_update_omnichannel_setting",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = omnichannelsettings.UpdateOmnichannelSettingRequest.pb(
            omnichannelsettings.UpdateOmnichannelSettingRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = omnichannelsettings.OmnichannelSetting.to_json(
            omnichannelsettings.OmnichannelSetting()
        )
        req.return_value.content = return_value

        request = omnichannelsettings.UpdateOmnichannelSettingRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = omnichannelsettings.OmnichannelSetting()
        post_with_metadata.return_value = (
            omnichannelsettings.OmnichannelSetting(),
            metadata,
        )

        client.update_omnichannel_setting(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_request_inventory_verification_rest_bad_request(
    request_type=omnichannelsettings.RequestInventoryVerificationRequest,
):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/omnichannelSettings/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        json_return_value = ""
        response_value.json = mock.Mock(return_value={})
        response_value.status_code = 400
        response_value.request = mock.Mock()
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        client.request_inventory_verification(request)


@pytest.mark.parametrize(
    "request_type",
    [
        omnichannelsettings.RequestInventoryVerificationRequest,
        dict,
    ],
)
def test_request_inventory_verification_rest_call_success(request_type):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )

    # send a request that will satisfy transcoding
    request_init = {"name": "accounts/sample1/omnichannelSettings/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = omnichannelsettings.RequestInventoryVerificationResponse()

        # Wrap the value into a proper Response obj
        response_value = mock.Mock()
        response_value.status_code = 200

        # Convert return value to protobuf type
        return_value = omnichannelsettings.RequestInventoryVerificationResponse.pb(
            return_value
        )
        json_return_value = json_format.MessageToJson(return_value)
        response_value.content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        response = client.request_inventory_verification(request)

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, omnichannelsettings.RequestInventoryVerificationResponse
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_request_inventory_verification_rest_interceptors(null_interceptor):
    transport = transports.OmnichannelSettingsServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.OmnichannelSettingsServiceRestInterceptor(),
    )
    client = OmnichannelSettingsServiceClient(transport=transport)

    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_request_inventory_verification",
    ) as post, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "post_request_inventory_verification_with_metadata",
    ) as post_with_metadata, mock.patch.object(
        transports.OmnichannelSettingsServiceRestInterceptor,
        "pre_request_inventory_verification",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        post_with_metadata.assert_not_called()
        pb_message = omnichannelsettings.RequestInventoryVerificationRequest.pb(
            omnichannelsettings.RequestInventoryVerificationRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = mock.Mock()
        req.return_value.status_code = 200
        req.return_value.headers = {"header-1": "value-1", "header-2": "value-2"}
        return_value = omnichannelsettings.RequestInventoryVerificationResponse.to_json(
            omnichannelsettings.RequestInventoryVerificationResponse()
        )
        req.return_value.content = return_value

        request = omnichannelsettings.RequestInventoryVerificationRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = omnichannelsettings.RequestInventoryVerificationResponse()
        post_with_metadata.return_value = (
            omnichannelsettings.RequestInventoryVerificationResponse(),
            metadata,
        )

        client.request_inventory_verification(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()
        post_with_metadata.assert_called_once()


def test_initialize_client_w_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    assert client is not None


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_get_omnichannel_setting_empty_call_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.get_omnichannel_setting), "__call__"
    ) as call:
        client.get_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.GetOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_list_omnichannel_settings_empty_call_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.list_omnichannel_settings), "__call__"
    ) as call:
        client.list_omnichannel_settings(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.ListOmnichannelSettingsRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_create_omnichannel_setting_empty_call_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.create_omnichannel_setting), "__call__"
    ) as call:
        client.create_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.CreateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_update_omnichannel_setting_empty_call_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.update_omnichannel_setting), "__call__"
    ) as call:
        client.update_omnichannel_setting(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.UpdateOmnichannelSettingRequest()

        assert args[0] == request_msg


# This test is a coverage failsafe to make sure that totally empty calls,
# i.e. request == None and no flattened fields passed, work.
def test_request_inventory_verification_empty_call_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the actual call, and fake the request.
    with mock.patch.object(
        type(client.transport.request_inventory_verification), "__call__"
    ) as call:
        client.request_inventory_verification(request=None)

        # Establish that the underlying stub method was called.
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        request_msg = omnichannelsettings.RequestInventoryVerificationRequest()

        assert args[0] == request_msg


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.OmnichannelSettingsServiceGrpcTransport,
    )


def test_omnichannel_settings_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OmnichannelSettingsServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_omnichannel_settings_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.shopping.merchant_accounts_v1beta.services.omnichannel_settings_service.transports.OmnichannelSettingsServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OmnichannelSettingsServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_omnichannel_setting",
        "list_omnichannel_settings",
        "create_omnichannel_setting",
        "update_omnichannel_setting",
        "request_inventory_verification",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_omnichannel_settings_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.shopping.merchant_accounts_v1beta.services.omnichannel_settings_service.transports.OmnichannelSettingsServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OmnichannelSettingsServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id="octopus",
        )


def test_omnichannel_settings_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.shopping.merchant_accounts_v1beta.services.omnichannel_settings_service.transports.OmnichannelSettingsServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OmnichannelSettingsServiceTransport()
        adc.assert_called_once()


def test_omnichannel_settings_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OmnichannelSettingsServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
    ],
)
def test_omnichannel_settings_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/content",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
        transports.OmnichannelSettingsServiceRestTransport,
    ],
)
def test_omnichannel_settings_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OmnichannelSettingsServiceGrpcTransport, grpc_helpers),
        (transports.OmnichannelSettingsServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_omnichannel_settings_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "merchantapi.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/content",),
            scopes=["1", "2"],
            default_host="merchantapi.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
    ],
)
def test_omnichannel_settings_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_omnichannel_settings_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.OmnichannelSettingsServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_omnichannel_settings_service_host_no_port(transport_name):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="merchantapi.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "merchantapi.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://merchantapi.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_omnichannel_settings_service_host_with_port(transport_name):
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="merchantapi.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "merchantapi.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://merchantapi.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_omnichannel_settings_service_client_transport_session_collision(
    transport_name,
):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = OmnichannelSettingsServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = OmnichannelSettingsServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.get_omnichannel_setting._session
    session2 = client2.transport.get_omnichannel_setting._session
    assert session1 != session2
    session1 = client1.transport.list_omnichannel_settings._session
    session2 = client2.transport.list_omnichannel_settings._session
    assert session1 != session2
    session1 = client1.transport.create_omnichannel_setting._session
    session2 = client2.transport.create_omnichannel_setting._session
    assert session1 != session2
    session1 = client1.transport.update_omnichannel_setting._session
    session2 = client2.transport.update_omnichannel_setting._session
    assert session1 != session2
    session1 = client1.transport.request_inventory_verification._session
    session2 = client2.transport.request_inventory_verification._session
    assert session1 != session2


def test_omnichannel_settings_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OmnichannelSettingsServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_omnichannel_settings_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OmnichannelSettingsServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
    ],
)
def test_omnichannel_settings_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OmnichannelSettingsServiceGrpcTransport,
        transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
    ],
)
def test_omnichannel_settings_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_account_path():
    account = "squid"
    expected = "accounts/{account}".format(
        account=account,
    )
    actual = OmnichannelSettingsServiceClient.account_path(account)
    assert expected == actual


def test_parse_account_path():
    expected = {
        "account": "clam",
    }
    path = OmnichannelSettingsServiceClient.account_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_account_path(path)
    assert expected == actual


def test_omnichannel_setting_path():
    account = "whelk"
    omnichannel_setting = "octopus"
    expected = "accounts/{account}/omnichannelSettings/{omnichannel_setting}".format(
        account=account,
        omnichannel_setting=omnichannel_setting,
    )
    actual = OmnichannelSettingsServiceClient.omnichannel_setting_path(
        account, omnichannel_setting
    )
    assert expected == actual


def test_parse_omnichannel_setting_path():
    expected = {
        "account": "oyster",
        "omnichannel_setting": "nudibranch",
    }
    path = OmnichannelSettingsServiceClient.omnichannel_setting_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_omnichannel_setting_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OmnichannelSettingsServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = OmnichannelSettingsServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = OmnichannelSettingsServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = OmnichannelSettingsServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = OmnichannelSettingsServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = OmnichannelSettingsServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = OmnichannelSettingsServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = OmnichannelSettingsServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = OmnichannelSettingsServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = OmnichannelSettingsServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OmnichannelSettingsServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OmnichannelSettingsServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OmnichannelSettingsServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OmnichannelSettingsServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close_grpc():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


@pytest.mark.asyncio
async def test_transport_close_grpc_asyncio():
    client = OmnichannelSettingsServiceAsyncClient(
        credentials=async_anonymous_credentials(), transport="grpc_asyncio"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close_rest():
    client = OmnichannelSettingsServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )
    with mock.patch.object(
        type(getattr(client.transport, "_session")), "close"
    ) as close:
        with client:
            close.assert_not_called()
        close.assert_called_once()


def test_client_ctx():
    transports = [
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = OmnichannelSettingsServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (
            OmnichannelSettingsServiceClient,
            transports.OmnichannelSettingsServiceGrpcTransport,
        ),
        (
            OmnichannelSettingsServiceAsyncClient,
            transports.OmnichannelSettingsServiceGrpcAsyncIOTransport,
        ),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
