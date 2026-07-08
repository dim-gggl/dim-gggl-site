import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { fetchJson } from "./api";

const LanguageContext = createContext(null);

const STORAGE_KEY = "dim-gggl-lang";

function initialLanguage() {
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (stored === "en" || stored === "fr") return stored;
  return (navigator.language || "en").toLowerCase().startsWith("fr")
    ? "fr"
    : "en";
}

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(initialLanguage);
  const [site, setSite] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchJson("/site/", { lang }).then((data) => {
      if (!cancelled) setSite(data);
    });
    return () => {
      cancelled = true;
    };
  }, [lang]);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.lang = lang;
  }, [lang]);

  const t = useCallback(
    (key, vars) => {
      let message = site?.ui?.[key] ?? key;
      if (vars) {
        for (const [name, value] of Object.entries(vars)) {
          message = message.replaceAll(`{${name}}`, value);
        }
      }
      return message;
    },
    [site]
  );

  const value = useMemo(
    () => ({
      lang,
      setLang,
      toggleLang: () => setLang((current) => (current === "fr" ? "en" : "fr")),
      ready: site !== null,
      t,
      person: site?.person ?? {},
      stats: site?.stats ?? {},
    }),
    [lang, site, t]
  );

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
