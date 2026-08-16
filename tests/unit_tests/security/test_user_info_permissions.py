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

from unittest.mock import MagicMock

from superset.security.manager import SupersetSecurityManager
from superset.views.user_info import UserInfoView


def _user_info_pvm(view_menu_name: str) -> MagicMock:
    """Build the permission/view the ``/user_info/`` route is gated on."""
    pvm = MagicMock()
    pvm.permission.name = f"can_{UserInfoView.list._permission_name}"
    pvm.view_menu.name = view_menu_name
    return pvm


def test_user_info_view_menu_does_not_collide_with_admin_only_view_menus() -> None:
    """Regression test: ``/user_info/`` must be reachable by Alpha and Gamma.

    Flask-AppBuilder resolves a view menu by name, so on a metadata database
    with a case-insensitive collation the row it finds may differ from the
    requested name only in case. A view menu whose name folds onto an entry of
    ``ADMIN_ONLY_VIEW_MENUS`` therefore inherits the Admin-only restriction and
    non-Admin roles never receive its permissions, which bounces them to the
    welcome page.
    """
    view_menu = UserInfoView.class_permission_name
    assert not {
        name
        for name in SupersetSecurityManager.ADMIN_ONLY_VIEW_MENUS
        if name.lower() == view_menu.lower()
    }


def test_user_info_permission_is_granted_to_alpha_and_gamma(app_context: None) -> None:
    """The permission behind ``/user_info/`` belongs to Alpha and Gamma."""
    from superset.extensions import appbuilder

    sm = SupersetSecurityManager(appbuilder)
    pvm = _user_info_pvm(UserInfoView.class_permission_name)

    assert sm._is_admin_only(pvm) is False
    assert sm._is_alpha_pvm(pvm) is True
    assert sm._is_gamma_pvm(pvm) is True
