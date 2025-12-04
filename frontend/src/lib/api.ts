/**
 * API configuration for frontend.
 * 
 * In development: uses localhost
 * In production (Vercel): uses ngrok URL stored in localStorage
 */

// Default API URL (local development)
const DEFAULT_API_URL = 'http://127.0.0.1:8000';

// Key for storing custom backend URL in localStorage
const BACKEND_URL_KEY = 'spotify_stats_backend_url';

/**
 * Get the current API URL.
 * Checks localStorage for custom URL, falls back to env variable or default.
 */
export function getApiUrl(): string {
  if (typeof window !== 'undefined') {
    const customUrl = localStorage.getItem(BACKEND_URL_KEY);
    if (customUrl) {
      return customUrl;
    }
  }
  return process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL;
}

/**
 * Set a custom backend URL (e.g., ngrok URL).
 */
export function setBackendUrl(url: string): void {
  if (typeof window !== 'undefined') {
    // Remove trailing slash
    const cleanUrl = url.replace(/\/$/, '');
    localStorage.setItem(BACKEND_URL_KEY, cleanUrl);
  }
}

/**
 * Clear custom backend URL (revert to default).
 */
export function clearBackendUrl(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(BACKEND_URL_KEY);
  }
}

/**
 * Check if using custom backend URL.
 */
export function isUsingCustomBackend(): boolean {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(BACKEND_URL_KEY) !== null;
  }
  return false;
}
