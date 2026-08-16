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
import { hydrateMetric } from '../DatasourceEditor';

test('reads certification and warning out of the dataset API extra string', () => {
  expect(
    hydrateMetric({
      metric_name: 'count',
      extra: JSON.stringify({
        certification: { certified_by: 'someone', details: 'foo' },
        warning_markdown: 'handle with care',
      }),
    }),
  ).toMatchObject({
    certified_by: 'someone',
    certification_details: 'foo',
    warning_markdown: 'handle with care',
  });
});

test('reads the warning from the explore datasource payload, which has no extra', () => {
  expect(
    hydrateMetric({
      metric_name: 'count',
      certified_by: 'someone',
      certification_details: 'foo',
      warning_markdown: 'handle with care',
    }),
  ).toMatchObject({
    certified_by: 'someone',
    certification_details: 'foo',
    warning_markdown: 'handle with care',
  });
});

test('falls back to the legacy warning_text column', () => {
  expect(
    hydrateMetric({
      metric_name: 'count',
      warning_text: 'handle with care',
    }).warning_markdown,
  ).toBe('handle with care');
});

test('prefers extra over the top level warning fields', () => {
  expect(
    hydrateMetric({
      metric_name: 'count',
      extra: JSON.stringify({ warning_markdown: 'from extra' }),
      warning_markdown: 'from payload',
      warning_text: 'from column',
    }).warning_markdown,
  ).toBe('from extra');
});

test('leaves the warning empty when no shape carries one', () => {
  expect(
    hydrateMetric({ metric_name: 'count', extra: '{}' }).warning_markdown,
  ).toBe('');
});
