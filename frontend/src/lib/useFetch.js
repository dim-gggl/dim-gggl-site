import { useEffect, useState } from "react";
import { fetchJson } from "./api";
import { useLanguage } from "./LanguageContext";

/**
 * Fetch an API endpoint, re-fetching when the language or params change.
 * Keeps the previous payload while reloading so page content never flashes.
 */
export function useFetch(path, params) {
  const { lang } = useLanguage();
  const [state, setState] = useState({ data: null, error: null });
  const paramsKey = JSON.stringify(params ?? {});

  useEffect(() => {
    let cancelled = false;
    fetchJson(path, { lang, params: JSON.parse(paramsKey) })
      .then((data) => {
        if (!cancelled) setState({ data, error: null });
      })
      .catch((error) => {
        if (!cancelled) setState({ data: null, error });
      });
    return () => {
      cancelled = true;
    };
  }, [path, lang, paramsKey]);

  return state;
}
