const API_BASE = "/api";

export async function fetchJson(path, { lang, params } = {}) {
  const url = new URL(`${API_BASE}${path}`, window.location.origin);
  if (lang) url.searchParams.set("lang", lang);
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value === undefined || value === null || value === "") continue;
      if (Array.isArray(value)) {
        value.forEach((item) => url.searchParams.append(key, item));
      } else {
        url.searchParams.set(key, value);
      }
    }
  }
  const response = await fetch(url);
  if (!response.ok) {
    const error = new Error(`API ${path} responded ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return response.json();
}
