export const API_BASE_URL_FALLBACK = '/api/v1'
export const DEV_PROXY_TARGET_FALLBACK = 'http://localhost:8000'

function readTrimmedEnvValue(env, key) {
  const value = env?.[key]

  if (typeof value !== 'string') {
    return ''
  }

  return value.trim()
}

export function resolveApiBaseUrl(env) {
  return readTrimmedEnvValue(env, 'VITE_API_BASE_URL') || API_BASE_URL_FALLBACK
}

export function resolveDevProxyTarget(env) {
  return readTrimmedEnvValue(env, 'VITE_API_PROXY_TARGET') || DEV_PROXY_TARGET_FALLBACK
}
