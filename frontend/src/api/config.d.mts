export type EnvLike = Record<string, string | boolean | undefined>

export declare const API_BASE_URL_FALLBACK: string
export declare const DEV_PROXY_TARGET_FALLBACK: string

export declare function resolveApiBaseUrl(env: EnvLike): string
export declare function resolveDevProxyTarget(env: EnvLike): string
