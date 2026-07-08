import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Loader from "./components/Loader";
import { useLanguage } from "./lib/LanguageContext";
import Home from "./pages/Home";
import Ai from "./pages/Ai";
import Cli from "./pages/Cli";
import DjangoPage from "./pages/DjangoPage";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import About from "./pages/About";
import Skills from "./pages/Skills";
import NotFound from "./pages/NotFound";

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
  }, [pathname]);
  return null;
}

export default function App() {
  const location = useLocation();
  const { ready } = useLanguage();

  if (!ready) {
    return (
      <div className="grain flex min-h-screen items-center justify-center bg-bg">
        <Loader />
      </div>
    );
  }

  return (
    <div className="grain flex min-h-screen flex-col bg-bg">
      <ScrollToTop />
      <Navbar />
      <div className="flex-1">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<Home />} />
            <Route path="/ai" element={<Ai />} />
            <Route path="/cli" element={<Cli />} />
            <Route path="/django" element={<DjangoPage />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/:slug" element={<ProjectDetail />} />
            <Route path="/about" element={<About />} />
            <Route path="/skills" element={<Skills />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AnimatePresence>
      </div>
      <Footer />
    </div>
  );
}
