import test from 'node:test'
import assert from 'node:assert/strict'

import {
  API_BASE_URL_FALLBACK,
  DEV_PROXY_TARGET_FALLBACK,
  resolveApiBaseUrl,
  resolveDevProxyTarget,
} from './config.mjs'

test('resolveApiBaseUrl uses configured value after trimming whitespace', () => {
  assert.equal(
    resolveApiBaseUrl({ VITE_API_BASE_URL: '  https://api.example.com/v1  ' }),
    'https://api.example.com/v1',
  )
})

test('resolveApiBaseUrl falls back to the local API prefix', () => {
  assert.equal(resolveApiBaseUrl({}), API_BASE_URL_FALLBACK)
  assert.equal(resolveApiBaseUrl({ VITE_API_BASE_URL: '   ' }), API_BASE_URL_FALLBACK)
})

test('resolveDevProxyTarget uses configured value after trimming whitespace', () => {
  assert.equal(
    resolveDevProxyTarget({ VITE_API_PROXY_TARGET: '  http://backend:8000  ' }),
    'http://backend:8000',
  )
})

test('resolveDevProxyTarget falls back to localhost backend', () => {
  assert.equal(resolveDevProxyTarget({}), DEV_PROXY_TARGET_FALLBACK)
  assert.equal(resolveDevProxyTarget({ VITE_API_PROXY_TARGET: '' }), DEV_PROXY_TARGET_FALLBACK)
})
