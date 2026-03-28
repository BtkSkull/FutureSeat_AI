import { Routes, Route } from "react-router-dom";
import Main from "./components/Main/Main";
import Rank from "./components/RankPage/Rank";
import About from "./components/About/About";
import Contact from "./components/Contact/contact";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/rank" element={<Rank />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
  );
}

export default App;