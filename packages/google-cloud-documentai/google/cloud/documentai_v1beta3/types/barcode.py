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
    package="google.cloud.documentai.v1beta3",
    manifest={
        "Barcode",
    },
)


class Barcode(proto.Message):
    r"""Encodes the detailed information of a barcode.

    Attributes:
        format_ (str):
            Format of a barcode. The supported formats are:

            -  ``CODE_128``: Code 128 type.
            -  ``CODE_39``: Code 39 type.
            -  ``CODE_93``: Code 93 type.
            -  ``CODABAR``: Codabar type.
            -  ``DATA_MATRIX``: 2D Data Matrix type.
            -  ``ITF``: ITF type.
            -  ``EAN_13``: EAN-13 type.
            -  ``EAN_8``: EAN-8 type.
            -  ``QR_CODE``: 2D QR code type.
            -  ``UPC_A``: UPC-A type.
            -  ``UPC_E``: UPC-E type.
            -  ``PDF417``: PDF417 type.
            -  ``AZTEC``: 2D Aztec code type.
            -  ``DATABAR``: GS1 DataBar code type.
        value_format (str):
            Value format describes the format of the value that a
            barcode encodes. The supported formats are:

            -  ``CONTACT_INFO``: Contact information.
            -  ``EMAIL``: Email address.
            -  ``ISBN``: ISBN identifier.
            -  ``PHONE``: Phone number.
            -  ``PRODUCT``: Product.
            -  ``SMS``: SMS message.
            -  ``TEXT``: Text string.
            -  ``URL``: URL address.
            -  ``WIFI``: Wifi information.
            -  ``GEO``: Geo-localization.
            -  ``CALENDAR_EVENT``: Calendar event.
            -  ``DRIVER_LICENSE``: Driver's license.
        raw_value (str):
            Raw value encoded in the barcode. For example:
            ``'MEBKM:TITLE:Google;URL:https://www.google.com;;'``.
    """

    format_: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value_format: str = proto.Field(
        proto.STRING,
        number=2,
    )
    raw_value: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
