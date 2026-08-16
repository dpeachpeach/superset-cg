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
import re

from werkzeug.utils import secure_filename

# All C0 (U+0000–U+001F) and C1 (U+007F–U+009F) control characters.
# Stripping every control char (including tab, LF, CR) keeps titles safe for
# SMTP headers, Content-Disposition filenames, and headless-browser document.title.
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")

# Export ZIPs nest these names under a root directory, so entries are kept well
# below the 255 character limit common to Windows and most filesystems to leave
# room for the enclosing path.
MAX_FILENAME_LENGTH = 200


def sanitize_title(title: str) -> str:
    """Remove all C0/C1 control characters from a title string."""
    return _CONTROL_CHARS_RE.sub("", title)


def get_filename(model_name: str, model_id: int, skip_id: bool = False) -> str:
    model_name = sanitize_title(model_name)
    slug = secure_filename(model_name)
    if not slug:
        return str(model_id)

    suffix = "" if skip_id else f"_{model_id}"
    slug = slug[: MAX_FILENAME_LENGTH - len(suffix)].rstrip("_")
    return f"{slug}{suffix}" if slug else str(model_id)
