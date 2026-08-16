# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Spec shape of to-many relationships in list/show responses.

Flask-AppBuilder builds the schemas behind ``list_columns``/``show_columns``
with ``fields.Nested(<schema instance>, many=...)``, taking ``many`` from the
SQLAlchemy relationship kind. A collection such as a dashboard's owners must
therefore be documented as an array; documenting it as a single object breaks
clients generated from the spec, which is what marshmallow 3 did because it
dropped ``many`` when ``Nested`` was handed a schema *instance*.
"""

from typing import Any

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import fields, Schema

from superset.openapi.manager import resolver


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.String()


def build_spec(schema: type[Schema], name: str) -> dict[str, Any]:
    spec = APISpec(
        title="Superset",
        version="v1",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin(schema_name_resolver=resolver)],
    )
    spec.components.schema(name, schema=schema)
    return spec.to_dict()["components"]["schemas"][name]["properties"]


def test_to_many_relationship_is_documented_as_an_array() -> None:
    class DashboardListSchema(Schema):
        owners = fields.Nested(UserSchema(), many=True)

    assert build_spec(DashboardListSchema, "DashboardList")["owners"] == {
        "type": "array",
        "items": {"$ref": "#/components/schemas/User"},
    }


def test_to_one_relationship_is_documented_as_an_object() -> None:
    class DashboardListSchema(Schema):
        changed_by = fields.Nested(UserSchema(), many=False)

    assert build_spec(DashboardListSchema, "DashboardList")["changed_by"] == {
        "$ref": "#/components/schemas/User"
    }
