/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import { utils, writeFile } from 'xlsx';
import { logging } from '@apache-superset/core/utils';
import exportPivotExcel from './downloadAsPivotExcel';

jest.mock('xlsx', () => ({
  utils: { table_to_book: jest.fn(() => ({})) },
  writeFile: jest.fn(),
}));

jest.mock('@apache-superset/core/utils', () => ({
  logging: {
    error: jest.fn(),
  },
}));

const mockTableToBook = utils.table_to_book as jest.Mock;
const mockWriteFile = writeFile as jest.Mock;

beforeEach(() => {
  jest.clearAllMocks();
  document.body.innerHTML = '';
});

test('exports the matched table', () => {
  document.body.innerHTML = '<table id="pivot-table"></table>';

  exportPivotExcel('#pivot-table', 'my-pivot');

  expect(mockTableToBook).toHaveBeenCalledWith(
    document.querySelector('#pivot-table'),
  );
  expect(mockWriteFile).toHaveBeenCalledWith({}, 'my-pivot.xlsx');
  expect(logging.error).not.toHaveBeenCalled();
});

test('logs an error and bails out when no element matches the selector', () => {
  exportPivotExcel('#missing-table', 'my-pivot');

  expect(mockTableToBook).not.toHaveBeenCalled();
  expect(mockWriteFile).not.toHaveBeenCalled();
  expect(logging.error).toHaveBeenCalledWith(
    '[exportPivotExcel] No element found for selector: "#missing-table"',
  );
});
